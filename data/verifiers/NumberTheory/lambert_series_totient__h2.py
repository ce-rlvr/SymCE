import sympy
from sympy.ntheory import totient
import math
import itertools
import functools

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        x = float(witness)
        h1 = math.isfinite(x)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            x = float(witness)
            # The conclusion is the equality: sum_{n=1}^infty phi(n) x^n / (1 - x^n) == x / (1 - x)^2
            # This equality holds if and only if |x| < 1.
            # For |x| >= 1, the series diverges (or has undefined terms), so the equality fails.
            neg_q = abs(x) >= 1.0
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number",
    "¬Q: The series does not equal x/(1-x)^2 (e.g., it diverges)"
]

N_HYP = 1
NEG_Q_INDEX = 1