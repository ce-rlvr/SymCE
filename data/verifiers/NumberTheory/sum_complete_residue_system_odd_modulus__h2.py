import sympy
from sympy import Integer
import math
import itertools
import functools

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (m, S) where m is an integer and S is a collection of integers.
    """
    try:
        if len(witness) != 2:
            return [False, False]
        m, S = witness
    except Exception:
        return [False, False]

    # Check Hypothesis 1: m is an odd positive integer
    try:
        h1 = isinstance(m, (int, Integer)) and m > 0 and m % 2 == 1
        if not isinstance(S, (list, tuple, set)):
            h1 = False
        else:
            for x in S:
                if not isinstance(x, (int, Integer)):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # Check Negated Conclusion: sum(S) is NOT congruent to 0 mod m
    try:
        neg_q = sum(S) % m != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m is an odd positive integer",
    "¬Q: sum(x in S) is not congruent to 0 mod m"
]

N_HYP = 1
NEG_Q_INDEX = 1