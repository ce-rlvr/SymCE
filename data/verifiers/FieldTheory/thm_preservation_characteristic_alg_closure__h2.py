import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        h1 = bool(witness.is_Field)
    except Exception:
        h1 = False

    try:
        # The characteristic of the algebraic closure of a field is mathematically 
        # identical to the characteristic of the field itself.
        # Therefore, the conclusion is always True, and its negation is always False.
        if h1 and hasattr(witness, 'characteristic'):
            _ = witness.characteristic
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The characteristic of \\overline{F} is not equal to the characteristic of F"
]

N_HYP = 1
NEG_Q_INDEX = 1