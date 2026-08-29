import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        k = sympy.sympify(witness)
        if not k.is_real or not k.is_finite:
            neg_q = True
        elif k <= 0:
            neg_q = True
        elif k == sympy.floor(k):
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True
    return [neg_q]

CONDITION_LABELS = ["\u00acQ: continued fraction is not as stated"]

N_HYP = 0
NEG_Q_INDEX = 0