import sympy
from sympy import *
import itertools
import math
import functools

# Top-level setup for standard finite rings Z/nZ
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should represent (R, I, J) where R is a commutative ring,
    and I, J are ideals of R.
    For simplicity, we expect R to be an integer n >= 2 (representing Z/nZ),
    and I, J to be lists of elements in 0..n-1.
    """
    try:
        if isinstance(witness, dict):
            R = witness['R']
            I = witness['I']
            J = witness['J']
        else:
            R, I, J = witness
    except Exception:
        return [False] * 5

    try:
        if isinstance(R, (int, sympy.Integer)) and R >= 2:
            n = int(R)
        elif isinstance(R, (list, tuple, set)) and set(int(x) for x in R) == set(range(len(R))) and len(R) >= 2:
            n = len(R)
        else:
            n = None
    except Exception:
        n = None

    # H1: R is a commutative ring
    h1 = (n is not None)

    # H2: I is an ideal of R
    try:
        if h1:
            I_set = set(I)
            h2 = True
            if not I_set:
                h2 = False
            else:
                for a in I_set:
                    if not isinstance(a, (int, sympy.Integer)) or a < 0 or a >= n:
                        h2 = False
                        break
                    for b in I_set:
                        if (a - b) % n not in I_set:
                            h2 = False
                    for r in range(n):
                        if (a * r) % n not in I_set:
                            h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: J is an ideal of R
    try:
        if h1:
            J_set = set(J)
            h3 = True
            if not J_set:
                h3 = False
            else:
                for a in J_set:
                    if not isinstance(a, (int, sympy.Integer)) or a < 0 or a >= n:
                        h3 = False
                        break
                    for b in J_set:
                        if (a - b) % n not in J_set:
                            h3 = False
                    for r in range(n):
                        if (a * r) % n not in J_set:
                            h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: I is not the zero ideal
    try:
        if h1 and h2:
            h4 = any(x % n != 0 for x in I_set)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: There exists an element in J that is NOT a zero-divisor in R
    try:
        neg_q = False
        if h1 and h3:
            for x in J_set:
                is_zd = False
                # x is a zero-divisor if there exists y != 0 such that x*y = 0
                for y in range(1, n):
                    if (x * y) % n == 0:
                        is_zd = True
                        break
                if not is_zd:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "H_4: I is not the zero ideal",
    "¬Q: There exists an element in J that is not a zero-divisor in R"
]

N_HYP = 4
NEG_Q_INDEX = 4