import math
import itertools
import functools
import sympy
from sympy import Rational, Integer, Symbol
from sympy.abc import x, y, z

# Top-level setup for witness evaluation
# (No specific named groups or matrices are needed for this ring theory theorem)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "If P is a prime ideal of height 1, then P is a principal ideal."
    (The true theorem requires the ring R to be a Unique Factorization Domain).
    """
    # The witness can be an ideal P, or a tuple (R, P)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, P = witness
    else:
        P = witness

    # H_1: P is a prime ideal of R
    try:
        if isinstance(P, dict):
            h1 = bool(P.get('is_prime', False))
        elif hasattr(P, 'is_prime'):
            val = P.is_prime
            h1 = bool(val() if callable(val) else val)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: The height of P is exactly 1
    try:
        if isinstance(P, dict) and 'height' in P:
            h2 = P.get('height') == 1
        elif hasattr(P, 'height'):
            val = P.height
            h2 = (val() if callable(val) else val) == 1
        elif type(P).__name__ == 'NumberFieldIdeal':
            # In a Dedekind domain (like a number ring), every non-zero prime ideal has height 1.
            if hasattr(P, 'is_zero'):
                val = P.is_zero
                is_zero = val() if callable(val) else val
                h2 = h1 and not is_zero
            else:
                h2 = h1
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: P is NOT a principal ideal
    try:
        if isinstance(P, dict):
            neg_q = not bool(P.get('is_principal', True))
        elif hasattr(P, 'is_principal'):
            val = P.is_principal
            neg_q = not bool(val() if callable(val) else val)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: The height of P is exactly 1",
    "¬Q: P is not a principal ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2