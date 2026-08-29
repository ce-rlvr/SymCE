import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named bindings are required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            n = witness['n']
        else:
            a, b, n = witness
    except Exception:
        return [False, False]

    # H_1: n is a positive integer
    try:
        h1 = (type(n) is int or isinstance(n, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # neg_Q: gcd(a^n, b^n) != gcd(a, b)^n
    try:
        left = sympy.gcd(a**n, b**n)
        right = sympy.gcd(a, b)**n
        neg_q = bool(sympy.simplify(left - right) != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: gcd(a^n, b^n) != gcd(a, b)^n"
]

N_HYP = 1
NEG_Q_INDEX = 1