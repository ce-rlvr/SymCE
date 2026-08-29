import sympy
from sympy.ntheory import jacobi_symbol

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # witness is expected to be a tuple (n, a, b)
        n, a, b = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (int(n) == n) and (n > 0) and (n % 2 == 1)
    except Exception:
        h1 = False

    try:
        h2 = (int(a) == a) and (int(b) == b)
    except Exception:
        h2 = False

    try:
        neg_q = bool(jacobi_symbol(int(a), int(n)) != jacobi_symbol(int(b), int(n)))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: a and b are integers",
    "¬Q: (a/n) != (b/n)"
]

N_HYP = 2
NEG_Q_INDEX = 2