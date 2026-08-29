import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'n'):
            n = int(witness.n)
        else:
            n = int(witness)
        # B_n is the Artin braid group on n strands, which is defined for n >= 1
        h1 = (n >= 1)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'n'):
            n = int(witness.n)
        else:
            n = int(witness)
        # The center of B_n is infinite cyclic for n >= 2.
        # For n = 1, B_1 is the trivial group, whose center is the trivial group (finite, not infinite cyclic).
        neg_q = (n < 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: B_n is the Artin braid group on n strands",
    "¬Q: The center of B_n is not an infinite cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1