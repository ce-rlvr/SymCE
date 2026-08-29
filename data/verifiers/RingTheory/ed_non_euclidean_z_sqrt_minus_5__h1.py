import sympy
from sympy import ZZ, QQ
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            neg_q = True
        else:
            neg_q = bool(getattr(witness, 'is_PID', False))
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["¬Q: R is a Euclidean domain"]
N_HYP = 0
NEG_Q_INDEX = 0