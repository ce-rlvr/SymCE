import sympy
import sympy.ntheory
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            d = witness.get('d')
            x = witness.get('x')
            y = witness.get('y')
        else:
            d, x, y = witness
    except Exception:
        return [False, False, False, False]

    def is_int(val):
        try:
            if isinstance(val, bool):
                return False
            return float(val) == float(int(val))
        except Exception:
            return False

    try:
        h1 = is_int(d) and float(d) > 0
    except Exception:
        h1 = False

    try:
        if is_int(d):
            d_int = int(d)
            if d_int == 0:
                h2 = True
            elif abs(d_int) > 1:
                h2 = True
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        h3 = is_int(x) and is_int(y)
    except Exception:
        h3 = False

    try:
        if is_int(d) and is_int(x) and is_int(y):
            neg_q = (int(x)**2 - int(d) * int(y)**2 == -1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: d is a positive integer",
    "H_2: There exists a prime p such that p divides d",
    "H_3: x and y are integers",
    "¬Q: x^2 - dy^2 == -1"
]

N_HYP = 3
NEG_Q_INDEX = 3