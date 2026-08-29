import sympy
from sympy.polys.domains import Domain

ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
GF2 = sympy.GF(2)
GF3 = sympy.GF(3)
GF5 = sympy.GF(5)
GF7 = sympy.GF(7)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, Domain)
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.is_Field)
    except Exception:
        h2 = False

    try:
        neg_q = not bool(witness.is_Field)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: Polynomial ring over R is a Euclidean domain",
    "¬Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2