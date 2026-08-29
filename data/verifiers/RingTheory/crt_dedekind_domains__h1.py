import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard variables for polynomial rings.
x, y, z = sp.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a dictionary with keys 'I' and 'factors',
    or a tuple (I, factors), representing an ideal and its prime factorization
    in a polynomial ring over Q.
    Example witness: {'I': x*y, 'factors': [(x, 1), (y, 1)]}
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            I_expr = witness.get('I')
            factors = witness.get('factors')
        elif isinstance(witness, tuple) and len(witness) == 2:
            I_expr, factors = witness
        else:
            I_expr, factors = None, None
    except Exception:
        I_expr, factors = None, None

    # Check H_1: I is a non-zero proper ideal of R
    if I_expr is not None:
        try:
            I_expr = sp.sympify(I_expr)
            symbols = list(I_expr.free_symbols)
            if not symbols:
                # In Q[X], non-zero constants are units, so they don't generate proper ideals.
                h1 = False
            else:
                h1 = (I_expr != 0) and not I_expr.is_number
        except Exception:
            h1 = False

    # Check H_2: I = P_1^{e_1} ... P_k^{e_k} is the unique prime factorization of I
    if I_expr is not None and factors is not None:
        try:
            if isinstance(factors, list) and len(factors) > 0:
                prod = sp.Integer(1)
                seen_ideals = []
                h2_ok = True
                for item in factors:
                    try:
                        if len(item) != 2:
                            h2_ok = False
                            break
                    except Exception:
                        h2_ok = False
                        break
                        
                    P_i, e_i = item
                    P_i = sp.sympify(P_i)
                    
                    e_i_sym = sp.sympify(e_i)
                    if not e_i_sym.is_Integer:
                        h2_ok = False
                        break
                    e_i = int(e_i_sym)
                    
                    if e_i < 1:
                        h2_ok = False
                        break
                        
                    # Check that P_i generates a distinct ideal from previously seen ones
                    for seen_P in seen_ideals:
                        ratio = sp.cancel(P_i / seen_P)
                        if ratio.is_number and ratio != 0:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
                    seen_ideals.append(P_i)
                    
                    # Check that P_i is a valid prime ideal generator in Q[X]
                    if P_i.is_number or not P_i.free_symbols:
                        h2_ok = False
                        break
                    
                    # Check irreducibility over Q
                    flist = sp.factor_list(P_i, domain='QQ')
                    if len(flist[1]) != 1 or flist[1][0][1] != 1:
                        h2_ok = False
                        break
                    
                    prod *= P_i**e_i
                
                if h2_ok:
                    # Check if I_expr equals the product of P_i^e_i up to a unit (constant)
                    ratio = sp.cancel(I_expr / prod)
                    if ratio.is_number and ratio != 0:
                        h2 = True
        except Exception:
            h2 = False

    # Check ¬Q: R/I is NOT isomorphic to the direct product of quotient rings prod_{i=1}^k R/P_i^{e_i}
    # This holds if and only if the ideals P_i^{e_i} are NOT pairwise comaximal.
    # Since P_i are prime, P_i^{e_i} are comaximal iff P_i are comaximal.
    if factors is not None:
        try:
            if isinstance(factors, list) and len(factors) > 1:
                all_symbols = set()
                for item in factors:
                    P_i = sp.sympify(item[0])
                    all_symbols.update(P_i.free_symbols)
                all_symbols = list(all_symbols)
                
                is_comaximal_all = True
                if not all_symbols:
                    is_comaximal_all = True
                else:
                    for i in range(len(factors)):
                        for j in range(i + 1, len(factors)):
                            P_i = sp.sympify(factors[i][0])
                            P_j = sp.sympify(factors[j][0])
                            # In Q[X], P_i and P_j are comaximal iff their Groebner basis is {1}
                            gb = sp.groebner([P_i, P_j], *all_symbols, domain='QQ')
                            if list(gb) != [1]:
                                is_comaximal_all = False
                                break
                        if not is_comaximal_all:
                            break
                
                if not is_comaximal_all:
                    neg_q = True
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a non-zero proper ideal of R",
    "H_2: I = P_1^{e_1} ... P_k^{e_k} is the unique prime factorization of I, where P_i are distinct prime ideals and e_i >= 1",
    "¬Q: R/I is NOT isomorphic to the direct product of quotient rings prod_{i=1}^k R/P_i^{e_i}"
]

N_HYP = 2
NEG_Q_INDEX = 2