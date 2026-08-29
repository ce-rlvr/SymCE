import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.fp_groups import FpGroup
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
        h1 = isinstance(witness, (PermutationGroup, FpGroup))
    except Exception:
        h1 = False

    try:
        # The Frattini subgroup \Phi(G) is the intersection of all maximal subgroups of G.
        # It is a characteristic subgroup of G, which implies it is ALWAYS a normal subgroup of G.
        # Therefore, the conclusion "\Phi(G) is a normal subgroup of G" is mathematically True for any group G.
        # Its negation is always False.
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: \\Phi(G) is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1