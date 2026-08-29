import sympy
from sympy import isprime

def conditions(witness):
    try:
        p = int(witness)
        neg_q = not isprime(abs(p))
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["¬Q: factor ring is not isomorphic to F_p polynomial ring"]
N_HYP = 0
NEG_Q_INDEX = 0