import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        # H_1: \widehat{G} is the Pontryagin dual of G
        # This implicitly requires G to be a locally compact abelian group.
        # Every finite abelian group is a locally compact abelian group,
        # and its Pontryagin dual is well-defined.
        h1 = isinstance(witness, PermutationGroup) and witness.is_abelian
    except Exception:
        h1 = False

    try:
        # ¬Q: \widehat{G} is not isomorphic as a topological group to the circle group S^1
        # The Pontryagin dual of a finite abelian group is isomorphic to the group itself,
        # hence it is finite. The circle group S^1 is infinite.
        # Therefore, they are never isomorphic for any finite group witness.
        neg_q = isinstance(witness, PermutationGroup)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: \widehat{G} is the Pontryagin dual of G",
    "¬Q: \widehat{G} is not isomorphic as a topological group to the circle group S^1"
]

N_HYP = 1
NEG_Q_INDEX = 1