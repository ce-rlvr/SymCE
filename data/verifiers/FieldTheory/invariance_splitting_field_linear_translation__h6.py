import sympy
from sympy import Poly, RootOf, primitive_element
from sympy.abc import x, y

# Top-level setup
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    try:
        F = witness.get('F')
        f = witness.get('f')
        c = witness.get('c')
        g = witness.get('g')
        E1 = witness.get('E_1')
        E2 = witness.get('E_2')
    except Exception:
        return [False] * 6

    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False

    # H_2: f(x) is a polynomial over F
    try:
        h2 = isinstance(f, Poly) and f.domain == F and f.is_univariate
    except Exception:
        h2 = False

    # H_3: c is an element of F
    try:
        h3 = c in F
    except Exception:
        h3 = False

    # H_4: g(x) = f(x - c)
    try:
        if isinstance(g, Poly) and g.domain == F and g.is_univariate and g.gen == f.gen:
            gen = f.gen
            expected_g_expr = f.as_expr().subs(gen, gen - c)
            expected_g = Poly(expected_g_expr, gen, domain=F)
            h4 = (g == expected_g)
        else:
            h4 = False
    except Exception:
        h4 = False

    # H_5: E_1 is a splitting field of f(x) over F
    try:
        h5 = False
        if E1 == F:
            roots_dict = sympy.roots(f.as_expr(), multiple=False)
            if sum(roots_dict.values()) == f.degree():
                h5 = True
        elif isinstance(E1, Poly) and E1.domain == F and E1.is_univariate and E1.is_irreducible:
            alpha = RootOf(E1, 0)
            _, factors = f.factor_list(extension=alpha)
            if all(fac.degree() == 1 for fac, mult in factors):
                roots_dict = sympy.roots(f.as_expr(), multiple=False)
                roots = list(roots_dict.keys())
                if sum(roots_dict.values()) == f.degree():
                    if not roots:
                        h5 = (E1.degree() == 1)
                    else:
                        minpoly, _ = primitive_element(roots, y)
                        h5 = (E1.degree() == minpoly.degree())
    except Exception:
        h5 = False

    # ¬Q: E_1 and E_2 are not isomorphic over F
    try:
        neg_q = False
        if E1 == E2:
            neg_q = False
        elif isinstance(E1, Poly) and isinstance(E2, Poly) and E1.domain == F and E2.domain == F:
            if E1.is_univariate and E2.is_univariate and E1.is_irreducible and E2.is_irreducible:
                if E1.degree() != E2.degree():
                    neg_q = True
                else:
                    beta = RootOf(E2, 0)
                    _, factors = E1.factor_list(extension=beta)
                    has_root = any(fac.degree() == 1 for fac, mult in factors)
                    neg_q = not has_root
            else:
                neg_q = True
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F",
    "H_3: c is an element of F",
    "H_4: g(x) = f(x - c)",
    "H_5: E_1 is a splitting field of f(x) over F",
    "¬Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 5
NEG_Q_INDEX = 5