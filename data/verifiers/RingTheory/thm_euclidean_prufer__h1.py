import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        neg_q = not bool(witness.is_PID)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a Prüfer domain"
]

N_HYP = 0
NEG_Q_INDEX = 0