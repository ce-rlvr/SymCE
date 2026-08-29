import sympy
from sympy import Poly, factor_list, Symbol, Rational, I, RootOf
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: g(x) is an irreducible polynomial over F",
    "H_3: g(x) has at least one root in K",
    "¬Q: g(x) does not split completely into linear factors over K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    if not isinstance(witness, (list, tuple)) or len(witness) != 3:
        return [False, False, False, False]
    
    g, alpha, var = witness
    
    try:
        p_g = Poly(g, var, domain='QQ')
        h1 = True
    except Exception:
        h1 = False

    try:
        fac = factor_list(g, var, domain='QQ')
        h2 = (len(fac[1]) == 1 and fac[1][0][1] == 1 and Poly(fac[1][0][0], var).degree() > 0)
    except Exception:
        h2 = False

    try:
        fac_ext = factor_list(g, var, extension=alpha)
        h3 = any(Poly(f, var).degree() == 1 for f, mult in fac_ext[1])
    except Exception:
        h3 = False

    try:
        fac_ext = factor_list(g, var, extension=alpha)
        splits_completely = all(Poly(f, var).degree() == 1 for f, mult in fac_ext[1])
        neg_q = not splits_completely
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]