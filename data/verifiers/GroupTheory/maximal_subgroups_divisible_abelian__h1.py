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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_divisible'):
            h1 = witness.is_divisible() if callable(witness.is_divisible) else bool(witness.is_divisible)
        elif hasattr(witness, 'order'):
            h1 = (witness.order() == 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'has_maximal_subgroup'):
            neg_q = witness.has_maximal_subgroup() if callable(witness.has_maximal_subgroup) else bool(witness.has_maximal_subgroup)
        elif hasattr(witness, 'maximal_subgroups'):
            subs = witness.maximal_subgroups() if callable(witness.maximal_subgroups) else witness.maximal_subgroups
            neg_q = len(subs) > 0
        elif hasattr(witness, 'order'):
            neg_q = (witness.order() > 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a divisible group",
    "¬Q: G has a maximal subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1