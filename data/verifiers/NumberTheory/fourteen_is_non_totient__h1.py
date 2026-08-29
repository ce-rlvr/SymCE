import sympy
from sympy.ntheory import totient

def conditions(witness):
    try:
        x = sympy.sympify(witness)
        if not x.is_integer:
            neg_q = False
        else:
            neg_q = bool(totient(x) == 14)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["¬Q: phi(x) == 14"]
N_HYP = 0
NEG_Q_INDEX = 0