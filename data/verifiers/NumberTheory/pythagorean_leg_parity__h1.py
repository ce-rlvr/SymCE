import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
        else:
            a, b, c = witness
    except Exception:
        return [False, False]

    # H_1: a^2 + b^2 = c^2
    try:
        diff = a**2 + b**2 - c**2
        if diff == 0:
            h1 = True
        else:
            diff_simp = sympy.simplify(diff)
            if diff_simp == 0:
                h1 = True
            else:
                try:
                    h1 = math.isclose(float(diff_simp), 0.0, abs_tol=1e-9)
                except Exception:
                    h1 = False
    except Exception:
        h1 = False

    # ¬Q: a and b are both odd integers
    def is_odd_integer(x):
        try:
            if isinstance(x, int):
                return x % 2 != 0
            if isinstance(x, sympy.Integer):
                return int(x) % 2 != 0
            if isinstance(x, float):
                return x.is_integer() and int(x) % 2 != 0
            if hasattr(x, 'is_Integer') and x.is_Integer:
                return int(x) % 2 != 0
            if hasattr(x, 'is_integer'):
                is_int = x.is_integer() if callable(x.is_integer) else x.is_integer
                if is_int:
                    return int(x) % 2 != 0
            return False
        except Exception:
            return False

    try:
        neg_q = is_odd_integer(a) and is_odd_integer(b)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a^2 + b^2 = c^2",
    "¬Q: a and b are both odd integers"
]

N_HYP = 1
NEG_Q_INDEX = 1