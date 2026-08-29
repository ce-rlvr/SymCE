import sympy
from sympy import Poly

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        p = Poly(witness, x)
        h1 = (p.domain == sympy.ZZ)
    except Exception:
        h1 = False

    h2 = h1

    try:
        if not h1:
            neg_q = False
        else:
            p = Poly(witness, x)
            if p.is_zero:
                neg_q = False
            else:
                c = p.content()
                neg_q = (abs(c) != 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: K is the fraction field of R",
    "¬Q: intersection of ideals is not equal"
]

N_HYP = 2
NEG_Q_INDEX = 2