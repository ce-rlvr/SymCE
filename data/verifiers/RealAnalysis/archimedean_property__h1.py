import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        x, y = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(x > 0)
    except Exception:
        h1 = False

    try:
        if hasattr(y, 'is_real') and y.is_real is not None:
            h2 = bool(y.is_real)
        else:
            h2 = isinstance(y, (int, float))
    except Exception:
        h2 = False

    try:
        neg_q = True
        if isinstance(x, (int, float, sympy.Rational, sympy.Float)) and isinstance(y, (int, float, sympy.Rational, sympy.Float)):
            if x > 0:
                neg_q = False
        else:
            for n in [1, 10, 100, 1000, 10**4, 10**5, 10**6, 10**9, 10**12, 10**15, 10**18, 10**21]:
                if bool(n * x > y):
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x > 0",
    "H_2: y is a real number",
    "¬Q: There does not exist a natural number n such that nx > y"
]

N_HYP = 2
NEG_Q_INDEX = 2