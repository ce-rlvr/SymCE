import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(b, (int, sympy.Integer)) and 
              isinstance(c, (int, sympy.Integer)) and 
              a > 0 and b > 0 and c > 0)
    except Exception:
        h1 = False

    try:
        e1_is_int = ((a - b + c) % 2 == 0)
        e2_is_int = ((-a + b + c) % 2 == 0)
        e3_is_int = ((a + b + c) % 2 == 0)
        all_integers = e1_is_int and e2_is_int and e3_is_int
        neg_q = not all_integers
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "¬Q: The exradii given by (a - b + c) / 2, (-a + b + c) / 2, and (a + b + c) / 2 are not all integers"
]

N_HYP = 1
NEG_Q_INDEX = 1