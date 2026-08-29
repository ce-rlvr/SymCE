import math
import sympy
from sympy import Rational, Integer

def get_int(w):
    if isinstance(w, bool):
        raise ValueError("Boolean is not a valid witness")
    if isinstance(w, int):
        return w
    if hasattr(w, 'is_integer') and w.is_integer:
        return int(w)
    if isinstance(w, float) and w.is_integer():
        return int(w)
    raise ValueError("Witness must be an integer")

def conditions(witness) -> list[bool]:
    try:
        d = get_int(witness)
        # H_1: Z adjoin sqrt(d) is a quadratic order over the integers.
        # This requires d to not be a perfect square of an integer.
        # If d >= 0 and is a perfect square, rank over Z is 1, not 2.
        h1 = not (d >= 0 and math.isqrt(d)**2 == d)
    except Exception:
        h1 = False

    try:
        d = get_int(witness)
        # ~Q: The group of units of Z adjoin sqrt(d) is NOT isomorphic to Z_2 x Z.
        # For an imaginary quadratic order (d < 0), the unit group is finite,
        # so it is never isomorphic to Z_2 x Z.
        neg_q = (d < 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Z adjoin sqrt d is a quadratic order (d is a non-square integer)",
    "not Q: The group of units is not isomorphic to Z_2 x Z"
]

N_HYP = 1
NEG_Q_INDEX = 1