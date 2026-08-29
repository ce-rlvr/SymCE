import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # C* is the multiplicative group of non-zero complex numbers.
        # This is a contextual hypothesis that defines C* for the conclusion.
        h2 = True
    except Exception:
        h2 = False

    try:
        # The character group of G is Hom(G, C*).
        # Since C* is abelian, any homomorphism factors through the abelianization G/[G,G].
        # Thus Hom(G, C*) is isomorphic to Hom(G/[G,G], C*).
        # For a finite abelian group A, Hom(A, C*) is isomorphic to A.
        # So the character group of G is isomorphic to G/[G,G].
        # G is isomorphic to its character group iff G is isomorphic to G/[G,G].
        # Since G is finite, this holds iff |G| == |G/[G,G]|, which means [G,G] is trivial,
        # so G must be abelian.
        # Therefore, G is NOT isomorphic to its character group iff G is NOT abelian.
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: C* is the multiplicative group of non-zero complex numbers",
    "¬Q: G is not isomorphic to its character group"
]

N_HYP = 2
NEG_Q_INDEX = 2