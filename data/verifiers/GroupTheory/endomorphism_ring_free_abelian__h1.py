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
V4 = DihedralGroup(2)  # Klein four-group
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
        # H_1: The rank of F is a finite integer n
        # Any finite group (such as a PermutationGroup in SymPy) is finitely generated,
        # meaning its rank (minimal number of generators or torsion-free rank) is a finite integer.
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # ¬Q: The endomorphism ring End(F) is NOT isomorphic to the matrix ring M_n(Z)
        # For any finite group F, End(F) is finite.
        # If F is non-trivial, End(F) has size > 1.
        # The matrix ring M_n(Z) is infinite for n >= 1, and has size 1 for n = 0.
        # Thus, End(F) is never isomorphic to M_n(Z) for any non-trivial finite group.
        # If F is trivial, End(F) has size 1 and M_0(Z) has size 1, so they are isomorphic.
        if isinstance(witness, PermutationGroup):
            neg_q = witness.order() > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The rank of F is a finite integer n",
    "¬Q: The endomorphism ring End(F) is not isomorphic to the matrix ring M_n(Z)"
]

N_HYP = 1
NEG_Q_INDEX = 1