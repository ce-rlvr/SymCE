import sympy
from sympy.ntheory import divisors, totient

def conditions(witness) -> list[bool]:
    # H_1: n is a positive integer
    try:
        h1 = (int(witness) == witness) and (witness > 0)
    except Exception:
        h1 = False

    # H_2: n \equiv 0 \pmod 2
    try:
        h2 = (witness % 2 == 0)
    except Exception:
        h2 = False

    # neg_Q: \sum_{d|n} (-1)^{n/d} \phi(d) != 0
    try:
        if h1:
            n = int(witness)
            s = sum(((-1) ** (n // d)) * totient(d) for d in divisors(n))
            neg_q = (s != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: n is congruent to 0 mod 2",
    "¬Q: sum_{d|n} (-1)^{n/d} phi(d) != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2