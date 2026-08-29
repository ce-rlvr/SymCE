import sympy
from sympy.combinatorics import PermutationGroup
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
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
        if h1:
            # Verify we can compute its order
            _ = witness.order()
    except Exception:
        h1 = False

    # ¬Q: The Fitting subgroup of G is not trivial
    # (i.e., there exists a non-trivial nilpotent normal subgroup)
    try:
        neg_q = False
        if h1:
            for N in witness.normal_subgroups():
                if N.order() > 1 and N.is_nilpotent:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The Fitting subgroup of G is not trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1