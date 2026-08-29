import math
import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
            d = witness['d']
            m = witness['m']
            x = witness['x']
            y = witness['y']
        elif hasattr(witness, 'a'):
            a = witness.a
            b = witness.b
            c = witness.c
            d = witness.d
            m = witness.m
            x = witness.x
            y = witness.y
        else:
            a, b, c, d, m, x, y = witness
    except Exception:
        return [False, False, False, False]

    try:
        def is_int(v):
            return isinstance(v, int) or isinstance(v, sympy.Integer)
        h1 = all(is_int(v) for v in (a, b, c, d, m, x, y)) and m > 0
    except Exception:
        h1 = False

    try:
        h2 = math.gcd(int(b), int(m)) == 1
    except Exception:
        h2 = False

    try:
        h3 = math.gcd(int(d), int(m)) == 1
    except Exception:
        h3 = False

    try:
        left = (int(x) - int(y)) % int(m) == 0
        right = (int(a) * int(d) - int(b) * int(c)) % int(m) == 0
        neg_q = (left != right)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c, d, m are integers with m > 0",
    "H_2: gcd(b, m) = 1",
    "H_3: gcd(d, m) = 1",
    "¬Q: (x = y mod m) is not equivalent to (ad = bc mod m)"
]

N_HYP = 3
NEG_Q_INDEX = 3