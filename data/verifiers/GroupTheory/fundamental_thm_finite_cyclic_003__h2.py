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

def conditions(witness) -> list[bool]:
    try:
        G, d = witness
        h1 = bool(G.is_cyclic) and isinstance(d, int)
    except Exception:
        h1 = False

    try:
        G, d = witness
        count = sum(1 for H in G.subgroups() if H.order() == d)
        neg_q = bool(count != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group and d is an integer",
    "¬Q: G does not have exactly one subgroup of order d"
]

N_HYP = 1
NEG_Q_INDEX = 1