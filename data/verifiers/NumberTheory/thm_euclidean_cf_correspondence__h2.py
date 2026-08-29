import sympy
from sympy import Rational
from sympy.ntheory import continued_fraction_iterator

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness['p']
            q = witness['q']
            a_list = witness['a_list']
        else:
            p, q, a_list = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(p, int) and isinstance(q, int) and p > 0 and q > 0
    except Exception:
        h1 = False

    try:
        cf = list(continued_fraction_iterator(Rational(p, q)))
        neg_q = (cf != list(a_list))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are positive integers",
    "¬Q: The finite simple continued fraction expansion of p/q is not exactly the given sequence"
]

N_HYP = 1
NEG_Q_INDEX = 1