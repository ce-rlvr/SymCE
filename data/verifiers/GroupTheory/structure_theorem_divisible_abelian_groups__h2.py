import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    # H_1: G is an abelian group
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # ¬Q: G is NOT isomorphic to a direct sum of copies of Q and Z(p^\infty)
    # Since Q and Z(p^\infty) are infinite groups, any non-empty direct sum of them is infinite.
    # Therefore, a finite group is isomorphic to such a direct sum if and only if it is the trivial group (empty sum).
    try:
        order = witness.order()
        if order == 1:
            neg_q = False
        elif order != sympy.oo and order > 1:
            neg_q = True
        else:
            # If the group is infinite, we cannot easily verify isomorphism in this context,
            # but we expect finite counterexamples (e.g., Z2).
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: G is not isomorphic to a direct sum of copies of Q and Z(p^\\infty)"
]

N_HYP = 1
NEG_Q_INDEX = 1