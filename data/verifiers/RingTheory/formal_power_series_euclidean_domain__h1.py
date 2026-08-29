import sympy
from sympy import ZZ, QQ

def conditions(witness):
    try:
        neg_q = not bool(witness.is_Field)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["¬Q: Formal power series ring over F is not a Euclidean domain"]
N_HYP = 0
NEG_Q_INDEX = 0