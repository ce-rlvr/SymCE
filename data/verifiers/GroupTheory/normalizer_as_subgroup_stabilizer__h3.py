import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: The stabilizer of H under the implicit conjugation action is not the normalizer N_G(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'is_group') or hasattr(G, 'elements') or isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = H.is_subgroup(G)
    except Exception:
        h2 = False

    # ¬Q: The conclusion FAILS at the witness.
    # The false conjecture omits the definition of the conjugation action (e.g., on the set of subgroups).
    # Without this, the "conjugation action" defaults to the standard pointwise conjugation on elements,
    # where the stabilizer is the centralizer C_G(H), not the normalizer N_G(H).
    # The conclusion fails when C_G(H) != N_G(H).
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            C = G.centralizer(H)
            N = G.normalizer(H)
            # The conclusion fails if the centralizer is strictly smaller than the normalizer
            neg_q = (C.order() != N.order())
    except Exception:
        # If the action is completely undefined or computation fails, the conclusion is invalid (fails).
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]