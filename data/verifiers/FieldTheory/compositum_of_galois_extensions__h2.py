import sympy

x, y = sympy.symbols('x y')

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K and L are contained in a common extension field",
    "H_3: K/F is a Galois extension",
    "H_4: L/F is a Galois extension",
    "¬Q: The compositum field KL is NOT a Galois extension of F"
]

N_HYP = 4
NEG_Q_INDEX = 4

def standardize_poly(p):
    if isinstance(p, str):
        p = sympy.sympify(p)
    if isinstance(p, (list, tuple, sympy.Tuple)):
        return sympy.Poly(p, x).as_expr()
    p = sympy.sympify(p)
    if isinstance(p, sympy.Eq):
        p = p.lhs - p.rhs
    syms = p.free_symbols
    if not syms:
        return p
    s = list(syms)[0]
    return p.subs(s, x)

def is_galois(p_expr):
    try:
        p = sympy.Poly(p_expr, x, domain='QQ')
        if p.degree() < 1:
            return False
        if not p.is_irreducible:
            return False
        r = sympy.CRootOf(p.as_expr(), 0)
        f_list = sympy.factor_list(p.as_expr(), extension=r)
        for fac, mult in f_list[1]:
            if sympy.Poly(fac, x).degree() > 1:
                return False
        return True
    except Exception:
        return False

def compositum_poly(p1_expr, p2_expr):
    best_fac = None
    max_deg = -1
    for k in range(1, 3):
        p1_sub = p1_expr.subs(x, x - k*y)
        p2_sub = p2_expr.subs(x, y)
        R = sympy.resultant(p1_sub, p2_sub, y)
        factors = sympy.factor_list(R)[1]
        for fac, mult in factors:
            d = sympy.Poly(fac, x).degree()
            if d > max_deg:
                max_deg = d
                best_fac = fac
    return best_fac

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False]*4 + [False]
        p1, p2 = witness
        p1 = standardize_poly(p1)
        p2 = standardize_poly(p2)
    except Exception:
        return [False]*4 + [False]

    # H1: F is a field (we fix F = QQ, which is a field)
    h1 = True

    # H2: K and L are contained in a common extension field (number fields are in CC)
    h2 = True

    # H3: K/F is a Galois extension
    try:
        h3 = is_galois(p1)
    except Exception:
        h3 = False

    # H4: L/F is a Galois extension
    try:
        h4 = is_galois(p2)
    except Exception:
        h4 = False

    # ¬Q: The compositum field KL is NOT a Galois extension of F
    try:
        comp = compositum_poly(p1, p2)
        if comp is None:
            neg_q = False
        else:
            neg_q = not is_galois(comp)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]