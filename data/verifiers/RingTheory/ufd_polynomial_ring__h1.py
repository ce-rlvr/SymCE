import sympy
from sympy import Symbol
from sympy.polys.domains import ZZ, QQ, EX

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        h1_ok = bool(witness.is_UFD)
    except Exception:
        h1_ok = False

    try:
        rx = witness.poly_ring(x)
        neg_q_ok = not bool(rx.is_UFD)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: The polynomial ring over R is not a Unique Factorization Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1