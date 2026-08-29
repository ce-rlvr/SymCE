import math

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, tuple) and len(witness) == 2 and type(witness[0]) is int and type(witness[1]) is int and witness[0] > 0 and witness[1] > 0
    except Exception:
        h1 = False

    try:
        k = math.gcd(witness[0], witness[1])
        neg_q = any((x * x) % k != x for x in range(k))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is the tensor product of R and S over Z (witness is (n, m) for Z_n, Z_m)",
    "¬Q: T is not a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1