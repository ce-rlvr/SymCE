import sympy
from sympy import Poly, QQ, ZZ, GF
from sympy.abc import x, y, z

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "H_3: m(x) is the minimal polynomial of alpha over F",
    "not Q: F(alpha) is not isomorphic to the quotient ring"
]

def conditions(witness):
    try:
        F = witness.get("F")
        E = witness.get("E")
        alpha = witness.get("alpha")
        m = witness.get("m")
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: E is an extension field of F
    try:
        h2 = False
        if h1 and getattr(E, 'is_Field', False):
            if getattr(F, 'characteristic', None) == getattr(E, 'characteristic', None):
                h2 = True
    except Exception:
        h2 = False

    # H_3: m(x) is the minimal polynomial of alpha over F
    try:
        h3 = False
        if m == 0 or (hasattr(m, 'is_zero') and m.is_zero):
            if hasattr(E, 'gens') and alpha in E.gens:
                h3 = True
            elif hasattr(alpha, 'is_Symbol') and alpha.is_Symbol:
                h3 = True
        else:
            m_poly = m if isinstance(m, Poly) else Poly(m, x, domain=F)
            if m_poly.is_monic and m_poly.is_irreducible:
                val = m_poly.eval(alpha)
                if val == 0 or (hasattr(val, 'is_zero') and val.is_zero):
                    h3 = True
    except Exception:
        h3 = False

    # neg_Q: F(alpha) is not isomorphic to F[x]/(m(x))
    try:
        neg_Q = False
        if m == 0 or (hasattr(m, 'is_zero') and m.is_zero):
            neg_Q = True
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]