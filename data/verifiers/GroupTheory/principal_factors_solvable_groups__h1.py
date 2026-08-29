import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)

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

def conditions(witness) -> list[bool]:
    try:
        # The conclusion is that every principal factor of G is an elementary abelian p-group.
        # For finite groups, this is exactly equivalent to G being solvable.
        # Therefore, the conclusion fails if and only if G is not solvable.
        if callable(witness.is_solvable):
            neg_q = not bool(witness.is_solvable())
        else:
            neg_q = not bool(witness.is_solvable)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G has a principal factor that is not an elementary abelian p-group (i.e. G is not solvable)"
]

N_HYP = 0
NEG_Q_INDEX = 0
