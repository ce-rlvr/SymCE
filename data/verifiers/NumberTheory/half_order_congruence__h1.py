import sympy
from sympy.ntheory import n_order
import math

# Top-level setup
# (No specific named objects needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        a, p = witness
        a = int(a)
        p = int(p)
    except Exception:
        return [False, False, False]

    # H_1: a is an integer not divisible by p
    try:
        h1 = (p != 0) and (a % p != 0)
    except Exception:
        h1 = False

    # H_2: The order of a modulo p is an even integer 2k
    k = None
    try:
        if p >= 2 and math.gcd(a, p) == 1:
            ord_a = n_order(a % p, p)
            if ord_a % 2 == 0:
                h2 = True
                k = ord_a // 2
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: a^k \not\equiv -1 \pmod p
    try:
        if k is not None and p != 0:
            val = pow(a % p, k, p)
            neg_q = ((val + 1) % p != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer not divisible by p",
    "H_2: The order of a modulo p is an even integer 2k",
    "¬Q: a^k is not congruent to -1 modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2