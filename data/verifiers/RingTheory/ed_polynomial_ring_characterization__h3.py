import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import Domain

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: Polynomial ring over R in one variable",
    "not Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, Domain)
        if h1 and hasattr(witness, 'mod'):
            from sympy import isprime
            h1 = bool(isprime(witness.mod))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(witness, Domain)
    except Exception:
        h2 = False

    try:
        neg_q = not bool(witness.is_Field)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]