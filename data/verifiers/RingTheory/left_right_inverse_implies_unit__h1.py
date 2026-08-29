import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture:
    Hypotheses:
      - a is an element of R
      - There exists an element b in R such that ba = 1
      - There exists an element c in R such that ac = 1
    Conclusion:
      - a is a unit in R and b = c.
    """
    try:
        if len(witness) == 3:
            a, b, c = witness
            has_e = False
        elif len(witness) == 4:
            a, b, c, e = witness
            has_e = True
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: a is an element of R
    try:
        _ = b * a
        _ = a * c
        h1 = True
    except Exception:
        h1 = False

    def is_id(x_val):
        if has_e:
            try:
                if x_val == e: return True
            except Exception:
                pass
        try:
            if x_val == 1: return True
        except Exception:
            pass
        try:
            if hasattr(x_val, 'is_Identity') and x_val.is_Identity: return True
        except Exception:
            pass
        try:
            if x_val == eye(x_val.shape[0]): return True
        except Exception:
            pass
        try:
            if x_val * a == a and a * x_val == a and x_val * b == b and x_val * c == c:
                return True
        except Exception:
            pass
        return False

    # H_2: There exists an element b in R such that ba = 1
    try:
        ba = b * a
        h2 = is_id(ba)
    except Exception:
        h2 = False

    # H_3: There exists an element c in R such that ac = 1
    try:
        ac = a * c
        h3 = is_id(ac)
    except Exception:
        h3 = False

    # ¬Q: a is not a unit in R or b != c
    try:
        neg_q = bool(b != c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of R",
    "H_2: There exists an element b in R such that ba = 1",
    "H_3: There exists an element c in R such that ac = 1",
    "¬Q: a is not a unit in R or b != c"
]

N_HYP = 3
NEG_Q_INDEX = 3