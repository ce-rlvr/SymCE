import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
        if len(witness) == 3:
            f_rank, m, n = witness
        elif len(witness) == 2:
            m, n = witness
            f_rank = 2
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(f_rank, int) and f_rank >= 1
    except Exception:
        h1 = False

    try:
        h2 = isinstance(m, int) and isinstance(n, int)
    except Exception:
        h2 = False

    try:
        neg_q = (m == 0 and abs(n) <= 1) or (n == 0 and abs(m) <= 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: BS(m,n) is the Baumslag-Solitar group",
    "¬Q: F contains a subgroup isomorphic to BS(m,n)"
]

N_HYP = 2
NEG_Q_INDEX = 2