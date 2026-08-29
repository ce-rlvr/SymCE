import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(3))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: N is a normal subgroup of A4
    try:
        h1 = False
        if isinstance(witness, PermutationGroup):
            is_sub = all(A4.contains(gen) for gen in witness.generators)
            if is_sub:
                a4_elements = list(A4.generate())
                is_normal = all(witness.contains(g * n * ~g) for g in a4_elements for n in witness.generators)
                h1 = is_normal
    except Exception:
        h1 = False

    # neg_Q: N does not have order 4 or is not isomorphic to the Klein four-group
    try:
        neg_q = True
        if isinstance(witness, PermutationGroup):
            order_4 = (witness.order() == 4)
            if order_4:
                witness_elements = list(witness.generate())
                is_v4 = all(g.order() in (1, 2) for g in witness_elements)
            else:
                is_v4 = False
            neg_q = not is_v4
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of A4",
    "¬Q: N does not have order 4 or is not isomorphic to the Klein four-group"
]

N_HYP = 1
NEG_Q_INDEX = 1