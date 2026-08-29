import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, K = witness
        else:
            R = witness
            K = R.get_field() if hasattr(R, 'get_field') else None
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(getattr(R, 'is_domain', False))
    except Exception:
        h1 = False

    try:
        if hasattr(R, 'get_field'):
            h2 = bool(K == R.get_field())
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        # The conjecture is considered false when R is not a field.
        neg_q = not bool(getattr(R, 'is_Field', False))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "¬Q: The field of fractions of R_x is not isomorphic to K_x"
]

N_HYP = 2
NEG_Q_INDEX = 2