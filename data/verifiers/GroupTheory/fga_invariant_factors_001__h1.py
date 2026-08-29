import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        # The conclusion states G is isomorphic to a direct product of cyclic groups.
        # All such direct products are abelian.
        # Therefore, if G is non-abelian, it cannot be isomorphic to such a product,
        # and the conclusion fails (neg_Q is True).
        # For finite groups (like SymPy's PermutationGroup), if it is abelian,
        # the Fundamental Theorem of Finite Abelian Groups guarantees the existence
        # and uniqueness of the invariant factors, so the conclusion holds (neg_Q is False).
        neg_q = not bool(witness.is_abelian)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is not isomorphic to Z^r x Z/d_1Z x ... x Z/d_kZ (e.g., G is non-abelian)"
]

N_HYP = 0
NEG_Q_INDEX = 0