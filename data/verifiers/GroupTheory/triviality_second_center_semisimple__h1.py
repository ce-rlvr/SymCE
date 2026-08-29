import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if h1:
            # Z_2(G) is defined as the preimage in G of the center of G/Z(G).
            # If Z(G) is trivial, G/Z(G) is isomorphic to G, so Z(G/Z(G)) is trivial,
            # and its preimage Z_2(G) is also trivial.
            # If Z(G) is non-trivial, Z_2(G) contains Z(G) and is therefore non-trivial.
            # Thus, Z_2(G) is non-trivial if and only if Z(G) is non-trivial.
            neg_q = bool(witness.center().order() > 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: Z_2(G) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1