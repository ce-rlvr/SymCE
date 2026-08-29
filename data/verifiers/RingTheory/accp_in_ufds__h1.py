import sympy
from sympy import Poly, Rational, cancel
from sympy.abc import x
import itertools

def in_R(expr):
    try:
        p = Poly(expr, x)
        if not all(isinstance(c, Rational) for c in p.coeffs()):
            return False
        const_term = p.nth(0)
        return const_term.is_integer
    except Exception:
        return False

def divides_in_R(a, b):
    try:
        if a == 0:
            return b == 0
        q = cancel(b / a)
        return in_R(q)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if callable(witness):
            seq = [witness(k) for k in range(1, 11)]
        else:
            seq = list(itertools.islice(witness, 10))
            if len(seq) < 10:
                return [False, False]
    except Exception:
        return [False, False]

    h1_ok = True
    for i in range(len(seq)):
        if not in_R(seq[i]):
            h1_ok = False
            break
        if i < len(seq) - 1:
            if not divides_in_R(seq[i+1], seq[i]):
                h1_ok = False
                break

    neg_q_ok = True
    for i in range(len(seq) - 1):
        if divides_in_R(seq[i], seq[i+1]):
            neg_q_ok = False
            break

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (a_k) is an ascending chain of principal ideals in R",
    "¬Q: The chain does not stabilize (strictly ascending)"
]

N_HYP = 1
NEG_Q_INDEX = 1