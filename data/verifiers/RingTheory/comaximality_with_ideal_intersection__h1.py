import sympy
from sympy import eye, zeros, Rational, Integer, Matrix
from sympy.abc import x, y, z
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        R, I, J, K = witness
    except Exception:
        return [False, False, False, False]
    
    def is_ring(R):
        if not R: return False
        # Check closure and commutativity of addition
        for a in R:
            for b in R:
                if (a - b) not in R: return False
                if (a * b) not in R: return False
                if a + b != b + a: return False
        # Check associativity and distributivity
        for a in R:
            for b in R:
                for c in R:
                    if (a + b) + c != a + (b + c): return False
                    if (a * b) * c != a * (b * c): return False
                    if a * (b + c) != (a * b) + (a * c): return False
                    if (a + b) * c != (a * c) + (b * c): return False
        return True

    def is_ideal(R, A):
        if not A: return False
        for a in A:
            if a not in R: return False
            for b in A:
                if (a - b) not in A: return False
            for r in R:
                if (a * r) not in A: return False
                if (r * a) not in A: return False
        return True

    def set_eq(A, B):
        for a in A:
            if a not in B: return False
        for b in B:
            if b not in A: return False
        return True

    def ideal_sum(A, B):
        res = []
        for a in A:
            for b in B:
                s = a + b
                if s not in res:
                    res.append(s)
        return res

    def ideal_int(A, B):
        res = []
        for a in A:
            if a in B and a not in res:
                res.append(a)
        return res

    try:
        h1 = is_ring(R) and is_ideal(R, I) and is_ideal(R, J) and is_ideal(R, K)
    except Exception:
        h1 = False

    try:
        h2 = set_eq(ideal_sum(I, J), R)
    except Exception:
        h2 = False

    try:
        h3 = set_eq(ideal_sum(I, K), R)
    except Exception:
        h3 = False

    try:
        neg_q = not set_eq(ideal_sum(I, ideal_int(J, K)), R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I, J, and K are ideals of R",
    "H_2: I and J are comaximal (I + J = R)",
    "H_3: I and K are comaximal (I + K = R)",
    "¬Q: I is not comaximal with J \\cap K (I + (J \\cap K) != R)"
]

N_HYP = 3
NEG_Q_INDEX = 3