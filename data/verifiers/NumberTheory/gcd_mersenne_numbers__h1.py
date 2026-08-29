import sympy
import math
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            m = witness.get('m')
            n = witness.get('n')
        else:
            a, m, n = witness
    except Exception:
        return [False, False, False]

    # H_1: a > 1
    try:
        h1 = bool(a > 1)
    except Exception:
        h1 = False

    # H_2: m and n are positive integers
    try:
        h2 = bool(isinstance(m, (int, Integer)) and isinstance(n, (int, Integer)) and m > 0 and n > 0)
    except Exception:
        h2 = False

    # ¬Q: gcd(a^m - 1, a^n - 1) != a^gcd(m, n) - 1
    try:
        val1 = a**m - 1
        val2 = a**n - 1
        g = sympy.gcd(val1, val2)
        expected = a**math.gcd(int(m), int(n)) - 1
        neg_q = bool(g != expected)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a > 1",
    "H_2: m and n are positive integers",
    "¬Q: gcd(a^m - 1, a^n - 1) != a^gcd(m, n) - 1"
]

N_HYP = 2
NEG_Q_INDEX = 2