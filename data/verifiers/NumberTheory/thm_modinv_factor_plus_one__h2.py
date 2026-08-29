import sympy
import math
import itertools
import functools

# No named bindings needed for this number theory conjecture; use integers directly.

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
        # Check if a and b are positive integers
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and a > 0 and b > 0
    except Exception:
        h1 = False

    try:
        a, b = witness
        m = a * b - 1
        # Calculate the modular inverse of a modulo m
        inv = sympy.mod_inverse(a, m)
        # The conclusion fails if the modular inverse is not b
        neg_q = (inv != b)
    except Exception:
        # If mod_inverse raises an exception (e.g., modulus is 0 or inverse doesn't exist),
        # then the modular inverse is certainly not b.
        try:
            a, b = witness
            neg_q = True
        except Exception:
            neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "¬Q: The modular inverse of a modulo a*b - 1 is not b"
]

N_HYP = 1
NEG_Q_INDEX = 1