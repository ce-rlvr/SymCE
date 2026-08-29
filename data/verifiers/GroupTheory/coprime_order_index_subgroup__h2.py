import math
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

def conditions(witness) -> list[bool]:
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2_ok = False

    try:
        h3_ok = (isinstance(N, PermutationGroup) and 
                 N.is_subgroup(G) and 
                 math.gcd(int(H.order()), int(G.order() // N.order())) == 1)
    except Exception:
        h3_ok = False

    try:
        neg_q_ok = not H.is_subgroup(N)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: The greatest common divisor of the order of H and the index of N in G is 1",
    "¬Q: H is not a subset of N"
]

N_HYP = 3
NEG_Q_INDEX = 3