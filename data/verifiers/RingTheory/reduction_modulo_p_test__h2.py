import sympy
from sympy.abc import x
from sympy.ntheory import isprime
from sympy import Poly, factor_list, QQ

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f_expr, p = witness
        f = Poly(f_expr, x)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = f.degree() >= 1 and f.domain == sympy.ZZ
    except Exception:
        h1 = False

    try:
        p_val = int(p)
        if p_val <= 1:
            h2 = False
        else:
            h2 = (f.LC() % p_val != 0)
    except Exception:
        h2 = False

    try:
        p_val = int(p)
        if p_val <= 1:
            h3 = False
        else:
            factors = factor_list(f, modulus=p_val)[1]
            h3 = (len(factors) == 1 and factors[0][1] == 1)
    except Exception:
        h3 = False

    try:
        factors = factor_list(f, domain=QQ)[1]
        is_irred = (len(factors) == 1 and factors[0][1] == 1)
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial in Z(x) of degree n >= 1",
    "H_2: p does not divide the leading coefficient of f(x)",
    "H_3: The reduction of f(x) modulo p is irreducible in Z_p(x)",
    "not Q: f(x) is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3