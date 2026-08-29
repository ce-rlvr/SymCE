import sympy
import math
import itertools
import functools

def conditions(witness):
    """
    Given a witness (p, k, d), checks if it is a valid counterexample.
    Returns [H_1, H_2, neg_Q].
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        p, k, d = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: k is a non-negative integer
    try:
        h2 = bool(isinstance(k, (int, sympy.Integer)) and k >= 0)
    except Exception:
        h2 = False

    # ¬Q: There is no integer j such that 0 <= j <= k and d = p^j
    try:
        neg_q = True
        if isinstance(k, (int, sympy.Integer)) and 0 <= k <= 100000:
            for j in range(int(k) + 1):
                if d == p**j:
                    neg_q = False
                    break
        else:
            # If k is not a valid integer or too large to iterate safely, 
            # we cannot verify the negated conclusion easily.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k is a non-negative integer",
    "¬Q: d != p^j for all integers j with 0 <= j <= k"
]

N_HYP = 2
NEG_Q_INDEX = 2