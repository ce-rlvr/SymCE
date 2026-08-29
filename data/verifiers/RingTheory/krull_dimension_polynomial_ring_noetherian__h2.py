import math
import sympy

SeidenbergRing = {"is_commutative": True, "dim_R": 1, "dim_Rx": 3}

def conditions(witness):
    try:
        h1 = bool(witness["is_commutative"])
    except Exception:
        h1 = False

    try:
        d = witness["dim_R"]
        h2 = isinstance(d, int) and d >= 0
    except Exception:
        h2 = False

    try:
        d = witness["dim_R"]
        d_x = witness["dim_Rx"]
        valid_dx = (d_x == math.inf) or (isinstance(d_x, int) and d_x >= 0)
        neg_q = valid_dx and (d_x != d + 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The Krull dimension of R is a finite integer d",
    "¬Q: The Krull dimension of the polynomial ring over R is not exactly d + 1"
]

N_HYP = 2
NEG_Q_INDEX = 2