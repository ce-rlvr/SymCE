import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    # H_1: G is a solvable group
    try:
        h1 = bool(witness.is_solvable)
    except Exception:
        h1 = False

    # ¬Q: There is NO non-negative integer n such that the n-th derived subgroup G^(n) is the trivial group.
    # In finite groups, the derived series always stabilizes. We check if the stabilized subgroup is non-trivial.
    try:
        ds = witness.derived_series()
        neg_q = bool(ds[-1].order() != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "¬Q: There is no non-negative integer n such that the n-th derived subgroup G^(n) is the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1