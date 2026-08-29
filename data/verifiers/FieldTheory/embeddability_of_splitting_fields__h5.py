import sympy
from sympy import Symbol, Poly, degree, sympify, roots, solve, QQ, ZZ, I, pi, exp, sqrt, Rational
from sympy.polys.numberfields import primitive_element

x = Symbol('x')

def get_gens(K):
    if isinstance(K, (list, tuple, set)):
        return list(K)
    if hasattr(K, 'orig_ext'):
        return list(K.orig_ext)
    if hasattr(K, 'gens'):
        return list(K.gens)
    return []

def extension_degree(gens):
    filtered = []
    for g in gens:
        g = sympify(g)
        if g.is_Rational:
            continue
        filtered.append(g)
    if not filtered:
        return 1
    v = Symbol('v')
    try:
        theta, minpoly = primitive_element(filtered, v)
        return degree(minpoly, v)
    except Exception:
        return None

def get_roots(f_expr, v):
    try:
        p = Poly(f_expr, v)
        rts_dict = roots(p)
        if sum(rts_dict.values()) == p.degree():
            return list(rts_dict.keys())
        rts = solve(f_expr, v)
        return rts
    except Exception:
        return []

def conditions(witness):
    try:
        F, f, E, K = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # H2: f is a polynomial over F
    try:
        if isinstance(f, Poly):
            v = f.gens[0]
            p = f
            f_expr = f.as_expr()
        else:
            f_expr = sympify(f)
            free = f_expr.free_symbols
            v = free.pop() if free else Symbol('x')
            p = Poly(f_expr, v)
            
        h2 = True
        for c in p.coeffs():
            try:
                F.from_expr(c)
            except Exception:
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: E is a splitting field of f over F
    try:
        F_gens = get_gens(F)
        E_gens = get_gens(E)
        abs_E_gens = F_gens + E_gens
        
        rts = get_roots(f_expr, v)
        
        deg_F = extension_degree(F_gens)
        deg_E = extension_degree(abs_E_gens)
        
        abs_split_gens = F_gens + rts
        deg_split = extension_degree(abs_split_gens)
        
        deg_E_roots = extension_degree(abs_E_gens + rts)
        
        h3 = (deg_E is not None) and (deg_split is not None) and \
             (deg_E == deg_split) and (deg_E_roots == deg_E) and \
             (len(rts) > 0) and (deg_E >= deg_F)
    except Exception:
        h3 = False

    # H4: K is an extension field of F
    try:
        K_gens = get_gens(K)
        abs_K_gens = F_gens + K_gens
        deg_K = extension_degree(abs_K_gens)
        h4 = (deg_K is not None) and (deg_K >= deg_F)
    except Exception:
        h4 = False

    # neg_Q: There does NOT exist an F-homomorphism from E into K
    try:
        deg_K_roots = extension_degree(abs_K_gens + rts)
        neg_q = (deg_K_roots is not None) and (deg_K_roots > deg_K)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: E is a splitting field of f over F",
    "H_4: K is an extension field of F",
    "neg_Q: There does NOT exist an F-homomorphism from E into K"
]

N_HYP = 4
NEG_Q_INDEX = 4