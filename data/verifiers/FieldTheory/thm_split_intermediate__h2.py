import sympy
from sympy import minpoly, degree, Rational, Poly, sqrt, I, Symbol
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

# Top-level setup for witness namespace
QQ = sympy.QQ
Q = sympy.QQ

def get_prim(gens):
    alg_gens = []
    seen = set()
    for g in gens:
        g_sym = sympy.nsimplify(sympy.sympify(g))
        if not g_sym.is_Rational:
            if g_sym not in seen:
                seen.add(g_sym)
                alg_gens.append(g_sym)
    if not alg_gens:
        return Rational(0)
    if len(alg_gens) == 1:
        return alg_gens[0]
    return primitive_element(alg_gens, ex=True)[0]

def field_degree(gens):
    p = get_prim(gens)
    if p == 0:
        return 1
    return degree(minpoly(p, x))

def in_field(val, gens):
    val = sympy.nsimplify(sympy.sympify(val))
    if val.is_Rational:
        return True
    d1 = field_degree(gens)
    d2 = field_degree(gens + [val])
    return d1 == d2

def parse_field(field_obj):
    if field_obj is sympy.QQ or str(field_obj) == "QQ":
        return []
    if isinstance(field_obj, (list, tuple, set)):
        return list(field_obj)
    return [field_obj]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = parse_field(witness.get("F", []))
            K = parse_field(witness.get("K", []))
            E = parse_field(witness.get("E", []))
            f = witness.get("f", x)
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            F = parse_field(witness[0])
            K = parse_field(witness[1])
            E = parse_field(witness[2])
            f = witness[3]
        else:
            return [False, False, False, False]
            
        f = sympy.sympify(f)
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    try:
        field_degree(F)
        h1 = True
    except Exception:
        h1 = False

    # H2: K is a splitting field of f(x) over F
    try:
        poly_f = Poly(f, x)
        roots_dict = sympy.roots(poly_f, x)
        if sum(roots_dict.values()) != poly_f.degree():
            h2 = False
        else:
            roots = list(roots_dict.keys())
            roots_in_K = all(in_field(r, K) for r in roots)
            K_in_F_roots = all(in_field(g, F + roots) for g in K)
            F_in_K = all(in_field(g, K) for g in F)
            h2 = roots_in_K and K_in_F_roots and F_in_K
    except Exception:
        h2 = False

    # H3: E is a subfield of K such that F is contained in E is contained in K
    try:
        F_in_E = all(in_field(g, E) for g in F)
        E_in_K = all(in_field(g, K) for g in E)
        h3 = F_in_E and E_in_K
    except Exception:
        h3 = False

    # NegQ: K is NOT a splitting field of f(x) viewed as a polynomial in E[x] over E
    try:
        poly_f = Poly(f, x)
        coeffs = poly_f.coeffs()
        f_in_E = all(in_field(c, E) for c in coeffs)
        
        roots_dict = sympy.roots(poly_f, x)
        roots = list(roots_dict.keys())
        
        K_in_E_roots = all(in_field(g, E + roots) for g in K)
        E_in_K_check = all(in_field(g, K) for g in E)
        
        splits_completely = (sum(roots_dict.values()) == poly_f.degree())
        roots_in_K = all(in_field(r, K) for r in roots)
        
        Q_holds = f_in_E and K_in_E_roots and E_in_K_check and splits_completely and roots_in_K
        neg_q = not Q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a splitting field of f over F",
    "H_3: E is a subfield of K containing F",
    "not_Q: K is not a splitting field of f over E"
]

N_HYP = 3
NEG_Q_INDEX = 3