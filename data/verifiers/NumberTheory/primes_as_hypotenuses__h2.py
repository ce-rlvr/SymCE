import math
from sympy import isprime

# Top-level setup
# (No named bindings needed for this domain)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        p = int(witness)
        count = 0
        p_sq = p**2
        limit = math.isqrt(p_sq // 2)
        for a in range(1, limit + 1):
            b_sq = p_sq - a**2
            b = math.isqrt(b_sq)
            if b**2 == b_sq:
                if a < b and math.gcd(a, math.gcd(b, p)) == 1:
                    count += 1
        neg_q = (count != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The number of positive integer pairs (a, b) with a < b, a^2 + b^2 = p^2, and gcd(a, b, p) = 1 is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1