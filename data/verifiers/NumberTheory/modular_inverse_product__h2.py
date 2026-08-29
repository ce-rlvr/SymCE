import sympy
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        m, a, b, c, d = witness
    except Exception:
        return [False, False, False, False]
        
    def check_equiv_1(val, mod):
        if hasattr(val, 'is_Matrix') and val.is_Matrix:
            I = sympy.eye(val.shape[0])
            diff = val - I
            for x in diff:
                if x % mod != 0:
                    return False
            return True
        else:
            return (val - 1) % mod == 0

    # H1: m is a positive integer
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and m > 0
    except Exception:
        h1 = False

    # H2: ab = 1 mod m
    try:
        h2 = check_equiv_1(a * b, m)
    except Exception:
        h2 = False

    # H3: cd = 1 mod m
    try:
        h3 = check_equiv_1(c * d, m)
    except Exception:
        h3 = False

    # neg_Q: (ac)(bd) != 1 mod m
    try:
        neg_q = not check_equiv_1((a * c) * (b * d), m)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: ab = 1 mod m",
    "H_3: cd = 1 mod m",
    "¬Q: (ac)(bd) != 1 mod m"
]

N_HYP = 3
NEG_Q_INDEX = 3