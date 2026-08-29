import sympy
from sympy.combinatorics import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if len(witness) == 5:
            F, x, y, z, n = witness
        elif len(witness) == 4:
            x, y, z, n = witness
            F = getattr(x, 'group', None)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = type(F).__name__ == "FreeGroup"
    except Exception:
        h1 = False

    try:
        if x in F and y in F:
            comm1 = x**-1 * y**-1 * x * y
            comm2 = x * y * x**-1 * y**-1
            h2 = (comm1 != F.identity) or (comm2 != F.identity)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        comm1 = x**-1 * y**-1 * x * y
        comm2 = x * y * x**-1 * y**-1
        h3 = isinstance(n, (int, sympy.Integer)) and (z**n == comm1 or z**n == comm2)
    except Exception:
        h3 = False

    try:
        neg_q = int(n) not in (1, -1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: x, y in F such that commutator of x and y is not 1",
    "H_3: n is an integer such that z^n is the commutator of x and y",
    "¬Q: n != 1 and n != -1"
]

N_HYP = 3
NEG_Q_INDEX = 3