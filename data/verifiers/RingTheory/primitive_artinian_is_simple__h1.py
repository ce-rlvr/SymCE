import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_right_primitive", False))
        else:
            val = getattr(witness, "is_right_primitive", False)
            h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get("is_simple", True))
        else:
            val = getattr(witness, "is_simple", True)
            neg_q = not bool(val() if callable(val) else val)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right primitive ring",
    "¬Q: R is not a simple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1