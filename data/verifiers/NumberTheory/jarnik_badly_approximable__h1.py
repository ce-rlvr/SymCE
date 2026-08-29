import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        neg_q = bool(sympy.S(witness) != 1)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["¬Q: The Hausdorff dimension of the set S is not exactly 1"]
N_HYP = 0
NEG_Q_INDEX = 0