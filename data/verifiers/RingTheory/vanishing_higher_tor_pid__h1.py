import sympy
from sympy import reduced, groebner, Expr
from sympy.abc import a, b, c, d, u, v, w, x, y, z

CONDITION_LABELS = [
    "H_1: M and N are arbitrary R-modules",
    "H_2: n >= 2 is an integer",
    "¬Q: Tor_n^R(M, N) is not identically zero"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Expects a witness representing a counterexample over a polynomial ring.
    Format: (R_vars, I_M, I_N, n) or a dict with these keys.
    - R_vars: list of variables (e.g., [x, y])
    - I_M: list of generators for the ideal defining module M = R/I_M
    - I_N: list of generators for the ideal defining module N = R/I_N
    - n: integer >= 2
    """
    try:
        if isinstance(witness, dict):
            R_vars = witness.get('R_vars', [])
            I_M = witness.get('I_M', [])
            I_N = witness.get('I_N', [])
            n = witness.get('n', 0)
        else:
            R_vars, I_M, I_N, n = witness
            
        R_vars = [sympy.sympify(var) for var in R_vars]
    except Exception:
        return [False, False, False]
        
    # H_1: M and N are arbitrary R-modules
    # We verify this by checking if I_M and I_N are valid lists of polynomials in R_vars
    try:
        def is_poly_in_vars(p, vars_list):
            try:
                if not isinstance(p, Expr):
                    return False
                return p.free_symbols.issubset(set(vars_list))
            except Exception:
                return False
                
        h1 = isinstance(I_M, (list, tuple)) and isinstance(I_N, (list, tuple))
        if h1:
            I_M = [sympy.sympify(p) for p in I_M]
            I_N = [sympy.sympify(p) for p in I_N]
            h1 = all(is_poly_in_vars(p, R_vars) for p in I_M) and \
                 all(is_poly_in_vars(p, R_vars) for p in I_N)
    except Exception:
        h1 = False
        
    # H_2: n >= 2 is an integer
    try:
        h2 = isinstance(n, int) and n >= 2
    except Exception:
        h2 = False
        
    # ¬Q: Tor_n^R(M, N) is not identically zero
    neg_q = False
    try:
        if h1 and h2:
            # To definitively prove Tor_n != 0 without a full resolution algorithm,
            # we check if I_M forms a regular sequence whose differentials vanish modulo I_N.
            # A simple sufficient condition for a regular sequence is that the generators
            # have pairwise disjoint sets of free symbols.
            is_reg_seq = True
            seen_vars = set()
            for p in I_M:
                fs = p.free_symbols
                if not fs:
                    is_reg_seq = False
                    break
                if not fs.issubset(set(R_vars)):
                    is_reg_seq = False
                    break
                if fs.intersection(seen_vars):
                    is_reg_seq = False
                    break
                seen_vars.update(fs)
                
            if is_reg_seq:
                dim = len(I_M)
                # If n <= projective dimension, Tor_n can be non-zero
                if n <= dim:
                    # Compute Groebner basis of I_N to check ideal membership
                    G = list(groebner(I_N, *R_vars))
                    
                    # Ensure 1 is not in I_N (so R/I_N is not the zero module)
                    _, rem1 = reduced(1, G, *R_vars)
                    if rem1 != 0:
                        # If all generators of I_M are in I_N, the differentials in the 
                        # Koszul complex tensored with R/I_N vanish completely.
                        all_in = True
                        for g in I_M:
                            _, rem = reduced(g, G, *R_vars)
                            if rem != 0:
                                all_in = False
                                break
                        
                        if all_in:
                            neg_q = True
    except Exception:
        pass
        
    return [h1, h2, neg_q]