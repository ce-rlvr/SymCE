import math
import sympy

Z = 0

def conditions(witness) -> list[bool]:
    try:
        n, x, y = witness
        h1 = isinstance(n, int) and (n == 0 or n >= 2)
    except Exception:
        h1 = False

    try:
        n, x, y = witness
        h2 = isinstance(n, int) and (n == 0 or n >= 2)
    except Exception:
        h2 = False

    try:
        n, x, y = witness
        h3 = isinstance(y, int) and isinstance(x, int)
    except Exception:
        h3 = False

    try:
        n, x, y = witness
        val = 1 - x * y
        if n == 0:
            neg_q = val not in (1, -1)
        else:
            neg_q = math.gcd(val % n, n) != 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity 1",
    "H_2: J(R) is the Jacobson radical of R",
    "H_3: y is an element of R",
    "¬Q: 1 - xy is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3