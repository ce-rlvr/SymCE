import sympy
from sympy import groebner, Poly, Matrix, diff
from sympy.abc import x, y, z, t, u, v, w
import itertools

# Top-level setup for standard symbols that might be used in the witness
# The witness is expected to be a local ring represented as a quotient of a polynomial ring localized at the origin.
# Format: witness = (vars, ideal_generators) or {'vars': [...], 'ideal': [...]}

def krull_dimension(ideal_gens, vars):
    """Computes the Krull dimension of the quotient ring k[vars]/ideal_gens at the origin."""
    if not ideal_gens:
        return len(vars)
    try:
        # Compute Groebner basis to find the initial ideal
        gb = groebner(ideal_gens, *vars, order='grlex')
        lms = []
        for g in gb:
            expr = g.as_expr() if hasattr(g, 'as_expr') else g
            if expr == 0:
                continue
            p = Poly(expr, *vars, order='grlex')
            if p.monoms():
                lms.append(p.monoms()[0])
    except Exception:
        return -1
    
    # The dimension is the maximum size of a subset of variables that is independent modulo the initial ideal
    for r in range(len(vars), -1, -1):
        for subset in itertools.combinations(range(len(vars)), r):
            independent = True
            for lm in lms:
                # Check if the leading monomial is supported only on the subset
                if all(lm[i] == 0 for i in range(len(vars)) if i not in subset):
                    independent = False
                    break
            if independent:
                return r
    return 0

def parse_witness(witness):
    if isinstance(witness, dict):
        vars_list = witness.get('vars', [])
        ideal_list = witness.get('ideal', [])
    elif isinstance(witness, (list, tuple)) and len(witness) == 2:
        vars_list, ideal_list = witness
    else:
        return None, None
    
    if not isinstance(vars_list, (list, tuple)):
        vars_list = [vars_list]
    if not isinstance(ideal_list, (list, tuple)):
        ideal_list = [ideal_list]
        
    return vars_list, ideal_list

def conditions(witness):
    vars_list, ideal_list = parse_witness(witness)
    if vars_list is None:
        return [False, False]
        
    # H_1: k = R/m is the residue field of R
    # This verifies that the witness represents a valid local ring at the origin.
    try:
        h1_ok = True
        if not vars_list:
            h1_ok = False
        for v_sym in vars_list:
            if not hasattr(v_sym, 'is_Symbol') or not v_sym.is_Symbol:
                h1_ok = False
        
        subs_dict = {v_sym: 0 for v_sym in vars_list}
        for gen in ideal_list:
            if gen.subs(subs_dict) != 0:
                h1_ok = False
    except Exception:
        h1_ok = False

    # not Q: The associated graded ring gr_m(R) is NOT isomorphic to a polynomial ring
    # This is equivalent to R NOT being a regular local ring, which means embedding_dimension > Krull_dimension.
    try:
        if not h1_ok:
            neg_q = False
        else:
            n = len(vars_list)
            # Compute the Jacobian matrix evaluated at the origin to find the embedding dimension
            J = Matrix([[diff(gen, v_sym) for v_sym in vars_list] for gen in ideal_list])
            J_0 = J.subs(subs_dict)
            rank_J0 = J_0.rank()
            emb_dim = n - rank_J0
            
            d = krull_dimension(ideal_list, vars_list)
            if d == -1:
                neg_q = False
            else:
                neg_q = bool(emb_dim > d)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: k = R/m is the residue field of R",
    "not Q: The associated graded ring is not isomorphic to a polynomial ring"
]

N_HYP = 1
NEG_Q_INDEX = 1