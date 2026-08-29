import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            G = witness[0]
        else:
            G = witness
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    h2_ok = True
    h3_ok = True
    neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: R(G) is the group ring of G over R",
    "H_3: Delta is the augmentation ideal of R(G)",
    "¬Q: The quotient ring R(G)/Delta is not isomorphic to R"
]

N_HYP = 3
NEG_Q_INDEX = 3