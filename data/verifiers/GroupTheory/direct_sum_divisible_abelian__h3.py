import math
import itertools
import functools
import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    # H_1: I is an index set
    try:
        h1_ok = isinstance(witness, (list, tuple, dict, set))
    except Exception:
        h1_ok = False

    # H_2: {D_i} is a family of abelian groups indexed by I
    try:
        if isinstance(witness, dict):
            groups = list(witness.values())
        elif isinstance(witness, (list, tuple, set)):
            groups = list(witness)
        else:
            groups = []
            
        h2_ok = h1_ok and all(
            isinstance(g, PermutationGroup) and getattr(g, 'is_abelian', False)
            for g in groups
        )
    except Exception:
        h2_ok = False

    # ¬Q: The direct sum ⊕_{i ∈ I} D_i is not a divisible abelian group
    # For finite groups, a group is divisible if and only if it is trivial (order 1).
    # Thus, the direct sum of finite groups is not divisible iff its order is > 1.
    try:
        if not h2_ok:
            neg_q_ok = False
        else:
            order_product = math.prod(g.order() for g in groups)
            neg_q_ok = order_product > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is an index set",
    "H_2: {D_i} is a family of abelian groups indexed by I",
    "¬Q: The direct sum ⊕_{i ∈ I} D_i is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2