import sympy
from sympy import Symbol
from sympy.ntheory import isprime

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(isprime(witness))
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p < 1:
            neg_q = False
        else:
            poly = sympy.cyclotomic_poly(p, x)
            factors = sympy.factor_list(poly, domain='QQ')
            is_irred = (len(factors[1]) == 1 and factors[1][0][1] == 1)
            neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: Phi_p(x) is not irreducible over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1