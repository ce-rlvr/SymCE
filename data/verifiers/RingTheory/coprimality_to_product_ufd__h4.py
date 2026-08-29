import sympy
import math
import itertools
import functools
from sympy import gcd
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False, False]

    try:
        def is_ufd_elem(val):
            if isinstance(val, (int, sympy.Integer)):
                return True
            if isinstance(val, sympy.Expr) and not getattr(val, 'is_Matrix', False):
                return True
            return False
        h1_ok = bool(is_ufd_elem(a) and is_ufd_elem(b) and is_ufd_elem(c))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool((a != 0) and (b != 0) and (c != 0))
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool(sympy.gcd(a, b) == 1)
    except Exception:
        h3_ok = False

    try:
        neg_q_ok = bool(sympy.gcd(a, b * c) != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, and c are non-zero elements of R",
    "H_3: a is coprime to b",
    "¬Q: a is not coprime to the product bc"
]

N_HYP = 3
NEG_Q_INDEX = 3