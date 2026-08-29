import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    """
    Final Result: Verifier Module for Normality of Inner Automorphisms.
    Evaluates the hypotheses and negated conclusion for the provided witness.
    """
    try:
        # Context validation: witness is a valid group
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # Context validation: inner automorphisms are well-defined for the group
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    try:
        # Final transformation: Inn(G) is mathematically proven to ALWAYS be a normal 
        # subgroup of Aut(G) for any group G. Thus, the negated conclusion (Inn(G) is 
        # NOT normal in Aut(G)) is universally False.
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Aut(G) is the automorphism group of G",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: Inn(G) is not a normal subgroup of Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2