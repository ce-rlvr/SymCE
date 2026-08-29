import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, bool):
            return [False]
        n = int(witness)
        if n != witness:
            return [False]
        
        # The conclusion states that there exist non-negative integers x, y such that n = x^2 - y^2.
        # Modulo 4, squares can only be 0 or 1. Thus, x^2 - y^2 mod 4 can only be 0, 1, or 3.
        # It can never be 2.
        # Conversely, any integer not congruent to 2 mod 4 can be written as a difference of two squares.
        # Therefore, the conclusion fails (neg_q is True) if and only if n % 4 == 2.
        neg_q = (n % 4 == 2)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: n cannot be written as x^2 - y^2 for non-negative integers x and y"
]

N_HYP = 0
NEG_Q_INDEX = 0