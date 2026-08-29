import sympy
from sympy import Poly, Symbol

x = Symbol('x')

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, Poly):
            p = witness
            if not p.domain.is_Field:
                p = p.set_domain('QQ')
        else:
            f = sympy.sympify(witness)
            p = Poly(f, x, domain='QQ')
        h1 = True
    except Exception:
        pass

    try:
        if h1:
            h2 = bool(p.is_univariate and p.degree() >= 1)
    except Exception:
        pass

    try:
        if h1 and h2:
            coeff, factors = sympy.factor_list(p)
            num_factors = sum(mult for _, mult in factors)
            neg_q = bool(num_factors > 1)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "H_2: f is non-constant", "not Q: ideal is not maximal"]
N_HYP = 2
NEG_Q_INDEX = 2