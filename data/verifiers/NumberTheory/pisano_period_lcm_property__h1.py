import math

def pisano_period(k):
    if k < 1:
        raise ValueError("k must be positive")
    if k == 1:
        return 1
    prev, curr = 0, 1
    # The Pisano period pi(k) is known to be at most 6k.
    for i in range(1, 6 * k + 2):
        prev, curr = curr, (prev + curr) % k
        if prev == 0 and curr == 1:
            return i
    return -1

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            h1 = False
        else:
            m, n = witness
            h1 = isinstance(m, int) and isinstance(n, int) and m >= 1 and n >= 1
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            m, n = witness
            pi_m = pisano_period(m)
            pi_n = pisano_period(n)
            pi_mn = pisano_period(m * n)
            lcm_val = (pi_m * pi_n) // math.gcd(pi_m, pi_n)
            neg_q = (pi_mn != lcm_val)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: pi(mn) != lcm(pi(m), pi(n))"
]

N_HYP = 1
NEG_Q_INDEX = 1