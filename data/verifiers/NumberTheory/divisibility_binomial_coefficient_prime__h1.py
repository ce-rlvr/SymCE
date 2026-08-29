import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            k = witness['k']
        else:
            p, k = witness
    except Exception:
        return [False, False]

    try:
        p_val = int(p)
        k_val = int(k)
        if p_val != p or k_val != k:
            h1 = False
        else:
            h1 = bool(0 < k_val < p_val)
    except Exception:
        h1 = False

    try:
        p_val = int(p)
        k_val = int(k)
        if p_val != p or k_val != k:
            neg_q = False
        elif p_val > 0 and k_val >= 0:
            neg_q = bool(math.comb(p_val, k_val) % p_val != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is an integer such that 0 < k < p",
    "¬Q: The binomial coefficient C(p, k) is not congruent to 0 (mod p)"
]

N_HYP = 1
NEG_Q_INDEX = 1