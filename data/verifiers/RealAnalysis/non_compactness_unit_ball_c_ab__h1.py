import math

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            h1 = False
        else:
            a, b = witness
            h1 = float(a) <= float(b)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            neg_q = False
        else:
            a, b = witness
            neg_q = float(a) == float(b)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: B is the closed unit ball in C(a, b)", "not Q: B is sequentially compact"]
N_HYP = 1
NEG_Q_INDEX = 1