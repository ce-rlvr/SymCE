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
        # The hypothesis simply defines Inn(G). We verify the witness is a valid finite group.
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # The hypothesis simply defines Out(G). We verify the witness is a valid finite group.
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    try:
        # Conclusion: Out(G) is isomorphic to Aut(G).
        # For finite groups, |Out(G)| = |Aut(G)| / |Inn(G)|.
        # Thus, Out(G) is isomorphic to Aut(G) if and only if |Inn(G)| = 1.
        # Since Inn(G) is isomorphic to G / Z(G), |Inn(G)| = 1 iff G is abelian.
        # Therefore, the conclusion fails (neg_q is True) iff G is NOT abelian.
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Inn(G) is the group of inner automorphisms of G",
    "H_2: Out(G) is the outer automorphism group of G, defined as the quotient group Aut(G)/Inn(G)",
    "¬Q: Out(G) is not isomorphic to Aut(G) (i.e., G is not abelian)"
]

N_HYP = 2
NEG_Q_INDEX = 2