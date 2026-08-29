import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple: (G, N1, N2)
    """
    try:
        G, N1, N2 = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(N1.is_subgroup(G) and N1.is_normal(G))
    except Exception:
        h1 = False

    try:
        h2 = bool(N2.is_subgroup(G) and N2.is_normal(G))
    except Exception:
        h2 = False

    try:
        # The conclusion states: G/(N_1 \cap N_2) is isomorphic to a subgroup of (G/N_1) \times (G/N_2).
        # By the First Isomorphism Theorem, the natural homomorphism from G to (G/N_1) \times (G/N_2)
        # given by g |-> (gN_1, gN_2) has kernel N_1 \cap N_2.
        # Thus, G/(N_1 \cap N_2) is ALWAYS isomorphic to the image of this homomorphism,
        # which is a subgroup of (G/N_1) \times (G/N_2).
        # This holds unconditionally for any group G and normal subgroups N_1, N_2.
        # Therefore, if N_1 and N_2 are normal subgroups, the conclusion is TRUE, so neg_Q is FALSE.
        # If they are not normal, the quotient groups are undefined, making the conclusion FALSE (neg_Q = TRUE).
        if h1 and h2:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N_1 is a normal subgroup of G",
    "H_2: N_2 is a normal subgroup of G",
    "¬Q: G/(N_1 \\cap N_2) is not isomorphic to a subgroup of (G/N_1) \\times (G/N_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2