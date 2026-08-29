import math

def P(k):
    if not isinstance(k, int) or k <= 0:
        return 0
    sq_freq = {}
    for x in range(k):
        s = (x * x) % k
        sq_freq[s] = sq_freq.get(s, 0) + 1
    
    total = 0
    for s1, f1 in sq_freq.items():
        for s2, f2 in sq_freq.items():
            s3 = (s1 + s2) % k
            f3 = sq_freq.get(s3, 0)
            total += f1 * f2 * f3
    return total

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            m = witness['m']
            n = witness['n']
        else:
            m, n = witness
        h1 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0 and (m * n <= 10000)
    except Exception:
        h1 = False

    try:
        if h1:
            neg_q = P(m * n) != P(m) * P(n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is a pair of positive integers (m, n)",
    "¬Q: P(mn) != P(m)P(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1