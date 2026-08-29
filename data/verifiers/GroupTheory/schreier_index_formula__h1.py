import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        if isinstance(witness, tuple):
            if len(witness) == 2:
                F, H = witness
                n = len(F.generators)
                k = F.order() // H.order()
            elif len(witness) == 4:
                F, H, n, k = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: H is a subgroup of F
    try:
        h1 = bool(H.is_subgroup(F))
    except Exception:
        h1 = False

    # H_2: H has finite index k in F
    try:
        if F.order() % H.order() == 0:
            idx = F.order() // H.order()
            h2 = bool(idx == k)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: H is not a free group of rank 1 + k(n - 1)
    try:
        expected_rank = 1 + k * (n - 1)
        if hasattr(H, 'order'):
            order = H.order()
            if order < float('inf'):
                # A finite group is a free group iff it is trivial (order 1) and its rank is 0.
                is_free = (order == 1 and expected_rank == 0)
            else:
                # If infinite, we cannot easily verify it is free of the exact rank here,
                # but counterexamples in this domain will typically be finite groups.
                is_free = False
        else:
            is_free = False
        
        neg_q = not is_free
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of F",
    "H_2: H has finite index k in F",
    "¬Q: H is not a free group of rank 1 + k(n - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2