import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
            p = witness.get('p', x**2 - y**2)
        elif hasattr(witness, 'x') and hasattr(witness, 'y'):
            x = witness.x
            y = witness.y
            p = getattr(witness, 'p', x**2 - y**2)
        elif len(witness) == 3:
            x, y, p = witness
        elif len(witness) == 2:
            x, y = witness
            p = x**2 - y**2
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        def is_pos_int(v):
            return isinstance(v, (int, sympy.Integer)) and not isinstance(v, bool) and v > 0
        h1 = bool(is_pos_int(x) and is_pos_int(y))
    except Exception:
        h1 = False

    try:
        h2 = bool(x**2 - y**2 == p)
    except Exception:
        h2 = False

    try:
        q = (x * 2 == p + 1) and (y * 2 == p - 1)
        neg_q = not bool(q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are positive integers",
    "H_2: x^2 - y^2 = p",
    "¬Q: x != (p+1)/2 or y != (p-1)/2"
]

N_HYP = 2
NEG_Q_INDEX = 2