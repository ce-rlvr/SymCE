import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok].
    """
    # H_1: G is a nilpotent group
    try:
        h1 = bool(witness.is_nilpotent)
    except Exception:
        h1 = False

    # H_2: Inn(G) is the group of inner automorphisms of G
    # This is a definitional hypothesis; we just verify the witness is a valid group.
    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # ¬Q: Inn(G) is NOT a nilpotent group of class c-1
    try:
        c = witness.nilpotency_class
        if c is None:
            neg_q = False
        else:
            # For a nilpotent group G of class c, Inn(G) is isomorphic to G/Z(G).
            # The nilpotency class of G/Z(G) is c - 1 if c >= 1, and 0 if c = 0.
            inn_class = max(0, c - 1)
            neg_q = bool(inn_class != c - 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: Inn(G) is not a nilpotent group of class c-1"
]

N_HYP = 2
NEG_Q_INDEX = 2