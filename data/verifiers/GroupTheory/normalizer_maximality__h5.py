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
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(K, PermutationGroup) and all(g in G for g in K.generators)
    except Exception:
        h3 = False

    try:
        h4 = all(g in K for g in H.generators)
    except Exception:
        h4 = False

    try:
        neg_q = False
        for k in K.generators:
            for h in H.generators:
                if (k * h * ~k) not in H:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "H_4: K contains H",
    "¬Q: K is not a subgroup of the normalizer N_G(H)"
]

N_HYP = 4
NEG_Q_INDEX = 4