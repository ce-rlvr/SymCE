import sympy
from sympy import *
import math

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def get_char(obj):
    """Helper to extract the characteristic from a ring object or integer."""
    if hasattr(obj, 'characteristic'):
        char = obj.characteristic
        if callable(char):
            return int(char())
        return int(char)
    if hasattr(obj, 'char'):
        char = obj.char
        if callable(char):
            return int(char())
        return int(char)
    return int(obj)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        R, S = witness
    except Exception:
        return [False, False, False, False]

    try:
        m = get_char(R)
        n = get_char(S)
    except Exception:
        return [False, False, False, False]

    # H_1: R and S are rings with identity
    # Interpreting integers m, n as the rings Z/mZ and Z/nZ (or Z if 0),
    # which are always rings with identity.
    try:
        h1 = (m >= 0 and n >= 0)
    except Exception:
        h1 = False

    # H_2: R has a non-zero characteristic m
    try:
        h2 = (m > 0)
    except Exception:
        h2 = False

    # H_3: S has a non-zero characteristic n
    try:
        h3 = (n > 0)
    except Exception:
        h3 = False

    # ¬Q: The characteristic n of S does not divide the characteristic m of R
    try:
        neg_q = (m % n != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: R has a non-zero characteristic m",
    "H_3: S has a non-zero characteristic n",
    "¬Q: The characteristic n of S does not divide the characteristic m of R"
]

N_HYP = 3
NEG_Q_INDEX = 3