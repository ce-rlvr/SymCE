import sympy
from sympy import gcd
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        n = witness
        # The conclusion is gcd(n, n^2 + 1) == 1.
        # The negated conclusion is gcd(n, n^2 + 1) != 1.
        val = gcd(n, n**2 + 1)
        neg_q = bool(val != 1)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: gcd(n, n^2+1) != 1"
]

N_HYP = 0
NEG_Q_INDEX = 0