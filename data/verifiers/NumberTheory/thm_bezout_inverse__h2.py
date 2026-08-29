import sympy
import math
import itertools
import functools

# No specific named bindings needed for this number theory conjecture.

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should be a dictionary {'a': a, 'x': x, 'n': n, 'y': y} or a tuple (a, x, n, y).
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            x = witness['x']
            n = witness['n']
            y = witness['y']
        else:
            a, x, n, y = witness
    except Exception:
        return [False, False, False]

    # H_1: n is an integer strictly greater than 1
    try:
        h1 = (int(n) == n) and (n > 1)
    except Exception:
        h1 = False

    # H_2: ax + ny = 1
    try:
        h2 = (a * x + n * y == 1)
    except Exception:
        h2 = False

    # ¬Q: x is not the modular inverse of a modulo n
    try:
        # To be "the" modular inverse, a, x, and n must be integers,
        # and x must be the canonical representative in the range [0, n-1].
        if int(a) != a or int(x) != x or int(n) != n:
            neg_q = True
        else:
            a_int = int(a)
            x_int = int(x)
            n_int = int(n)
            # pow(a, -1, n) computes the canonical modular inverse in [0, n-1]
            canonical_inv = pow(a_int, -1, n_int)
            neg_q = (x_int != canonical_inv)
    except Exception:
        # If modular inverse fails to compute (e.g., no inverse exists), x is not the inverse.
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: ax + ny = 1",
    "¬Q: x is not the modular inverse of a modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2