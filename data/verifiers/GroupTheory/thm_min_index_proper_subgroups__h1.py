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
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(G.order() > 1)
    except Exception:
        h1_ok = False

    try:
        is_subgroup = all(g in G for g in H.generators)
        is_proper = H.order() < G.order()
        h2_ok = bool(is_subgroup and is_proper)
    except Exception:
        h2_ok = False

    try:
        index = G.order() / H.order()
        neg_q_ok = bool(index < 5)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is not the trivial group",
    "H_2: H is a proper subgroup of G",
    "not Q: The index of H in G is less than 5"
]

N_HYP = 2
NEG_Q_INDEX = 2