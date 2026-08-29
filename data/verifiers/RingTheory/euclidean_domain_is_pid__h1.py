import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
ZZ_x_y = ZZ.poly_ring(x, y)
QQ_x_y = QQ.poly_ring(x, y)

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, 'is_PID'):
            return [False]
        is_pid = witness.is_PID
        if is_pid is None:
            return [False]
        neg_q = not is_pid
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 0
NEG_Q_INDEX = 0