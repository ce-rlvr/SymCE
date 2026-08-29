import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        n, d = witness
    except Exception:
        return [False, False]

    try:
        # H_1: n = sum_{i=0}^k d_i 10^i
        n_calc = sum(sympy.Rational(x) * (10**i) for i, x in enumerate(d))
        h1 = bool(sympy.Rational(n) == n_calc)
    except Exception:
        h1 = False

    try:
        # ¬Q: n is not congruent to sum(d) mod 9
        # Congruence mod 9 means (n - sum(d)) / 9 is an integer.
        diff = sympy.Rational(n) - sum(sympy.Rational(x) for x in d)
        q = (diff / 9).is_integer
        neg_q = not bool(q)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n = sum_{i=0}^k d_i 10^i",
    "¬Q: n is not congruent to sum(d) mod 9"
]

N_HYP = 1
NEG_Q_INDEX = 1