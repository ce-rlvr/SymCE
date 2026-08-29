import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        h1 = isinstance(witness, Permutation)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            h2 = bool(witness.order() % 2 == 1)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1:
            neg_q = not bool(witness.is_even)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is an element of S_n",
    "H_2: the order of sigma is an odd integer",
    "¬Q: sigma is not an even permutation"
]

N_HYP = 2
NEG_Q_INDEX = 2