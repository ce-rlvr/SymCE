import math
from sympy.ntheory import n_order

# Top-level setup
# No specific named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = int(witness['n'])
            a = int(witness['a'])
            b = int(witness['b'])
            d1 = int(witness['d1'])
            d2 = int(witness['d2'])
            k = int(witness['k'])
            m = int(witness['m'])
        else:
            n, a, b, d1, d2, k, m = [int(x) for x in witness]
    except Exception:
        return [False] * 6

    # H1: n >= 2 is an integer
    try:
        h1 = (n >= 2)
    except Exception:
        h1 = False

    # H2: a and b are integers coprime to n
    try:
        h2 = (math.gcd(a, n) == 1) and (math.gcd(b, n) == 1)
    except Exception:
        h2 = False

    # H3: d2 is the multiplicative order of b modulo n
    try:
        h3 = (d2 == n_order(b, n))
    except Exception:
        h3 = False

    # H4: gcd(d1, d2) == 1
    try:
        h4 = (math.gcd(d1, d2) == 1)
    except Exception:
        h4 = False

    # H5: a^k == b^m (mod n)
    try:
        h5 = (pow(a, k, n) == pow(b, m, n))
    except Exception:
        h5 = False

    # neg_Q: not (a^k == 1 (mod n) and b^m == 1 (mod n))
    try:
        q = (pow(a, k, n) == 1) and (pow(b, m, n) == 1)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: a and b are integers coprime to n",
    "H_3: d2 is the multiplicative order of b modulo n",
    "H_4: gcd(d1, d2) == 1",
    "H_5: a^k == b^m (mod n)",
    "¬Q: a^k != 1 (mod n) or b^m != 1 (mod n)"
]

N_HYP = 5
NEG_Q_INDEX = 5