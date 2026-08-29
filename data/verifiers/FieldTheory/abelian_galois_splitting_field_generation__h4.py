import sympy
from sympy import Poly, Symbol, factor_list, RootOf

x = Symbol('x')

def conditions(witness):
    try:
        p = Poly(witness, x, domain='QQ')
        h1 = p.domain.is_Field
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            factors = factor_list(p)
            is_irreducible = (len(factors[1]) == 1 and factors[1][0][1] == 1 and p.degree() > 0)
            is_separable = p.degree() > 0 and p.gcd(p.diff()).degree() == 0
            h2 = is_irreducible and is_separable
    except Exception:
        h2 = False

    try:
        h3 = h1 and p.degree() > 0
    except Exception:
        h3 = False

    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            r = RootOf(p.as_expr(), 0)
            ext_factors = factor_list(p.as_expr(), extension=r)
            num_factors = sum(mult for fac, mult in ext_factors[1])
            neg_q = num_factors < p.degree()
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is an irreducible separable polynomial over K",
    "H_3: L is the splitting field of f over K",
    "¬Q: For some root alpha in L, the splitting field L is not equal to K(alpha)"
]

N_HYP = 3
NEG_Q_INDEX = 3