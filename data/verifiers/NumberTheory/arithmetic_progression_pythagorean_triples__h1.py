import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named bindings required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple or list of three integers: (a, b, c)
        if len(witness) != 3:
            return [False, False]
        a, b, c = witness
        
        # Ensure they are integers
        if int(a) != a or int(b) != b or int(c) != c:
            return [False, False]
        a, b, c = int(a), int(b), int(c)
    except Exception:
        return [False, False]

    try:
        h1 = bool(b - a == c - b)
    except Exception:
        h1 = False

    try:
        # Check if there exists a positive integer k such that a = 3k, b = 4k, c = 5k
        q = (a % 3 == 0) and (a // 3 > 0) and (b == 4 * (a // 3)) and (c == 5 * (a // 3))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: b - a = c - b",
    "¬Q: There does not exist a positive integer k such that a = 3k, b = 4k, and c = 5k"
]

N_HYP = 1
NEG_Q_INDEX = 1