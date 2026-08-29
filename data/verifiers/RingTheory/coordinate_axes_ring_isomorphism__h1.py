import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
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

def conditions(witness):
    try:
        neg_Q = True
        if hasattr(witness, 'has_identity'):
            neg_Q = not witness.has_identity
    except Exception:
        neg_Q = True
    return [bool(neg_Q)]

CONDITION_LABELS = ['not Q: The factor ring is not isomorphic to the subring']

N_HYP = 0
NEG_Q_INDEX = 0