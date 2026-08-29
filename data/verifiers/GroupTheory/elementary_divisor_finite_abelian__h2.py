import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup) and witness.order() > 0
    except Exception:
        h1 = False

    try:
        # A direct product of cyclic groups is always abelian.
        # By the Fundamental Theorem of Finite Abelian Groups, every finite abelian group 
        # has a unique such decomposition. Thus, the conclusion holds if and only if G is abelian.
        # The conclusion fails (neg_Q is True) if and only if G is non-abelian.
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not isomorphic to a direct product of cyclic groups of prime-power orders"
]

N_HYP = 1
NEG_Q_INDEX = 1