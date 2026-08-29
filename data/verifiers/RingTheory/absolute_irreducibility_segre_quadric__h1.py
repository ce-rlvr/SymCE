import sympy as sp

def conditions(witness):
    try:
        w = int(witness)
        neg_q = (w > 1 and not sp.isprime(w))
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["not_Q: XY - ZW is not absolutely irreducible"]
N_HYP = 0
NEG_Q_INDEX = 0