import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, sympy.combinatorics.PermutationGroup)
        if h1:
            if callable(witness.order):
                h1 = h1 and (witness.order() > 0)
            else:
                h1 = h1 and (witness.order > 0)
    except Exception:
        h1 = False

    # ¬Q: G is not a nilpotent group
    try:
        nilp = witness.is_nilpotent
        if callable(nilp):
            neg_q = not nilp()
        else:
            neg_q = not nilp
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1