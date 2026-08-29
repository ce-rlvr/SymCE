import sympy
from sympy import ZZ, QQ

def conditions(witness):
    try:
        h1_ok = bool(witness.is_PID)
    except Exception:
        h1_ok = False

    try:
        # The formal power series ring over R is a PID if and only if R is a field.
        neg_q_ok = bool(witness.is_Field)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The formal power series ring over R is a principal ideal domain"
]

N_HYP = 1
NEG_Q_INDEX = 1