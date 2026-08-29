import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup

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

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # If it is a group, Inn(G) is well-defined as the group of inner automorphisms
        h2 = h1
    except Exception:
        h2 = False

    try:
        # The conclusion is: G is an abelian group, and Inn(G) is the trivial group.
        # Inn(G) is isomorphic to G/Z(G), which is trivial if and only if G is abelian.
        # Therefore, the conclusion holds iff G is abelian.
        # The negated conclusion holds iff G is NOT abelian.
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: G is not an abelian group or Inn(G) is not the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2