import sympy
from sympy.abc import x

ZZ = sympy.polys.domains.ZZ
QQ = sympy.polys.domains.QQ

def conditions(witness) -> list[bool]:
    try:
        R_x = witness.poly_ring(x)
        neg_q = not bool(R_x.is_UFD)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["not Q: The polynomial ring over R is not a Unique Factorization Domain"]

N_HYP = 0
NEG_Q_INDEX = 0