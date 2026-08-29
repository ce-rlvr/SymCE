import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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
        G, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a non-trivial group
    try:
        h2 = h1 and G.order() > 1
    except Exception:
        h2 = False

    # H_3: H is a proper subgroup of G
    try:
        h3 = isinstance(H, PermutationGroup) and H.is_subgroup(G) and H.order() < G.order()
    except Exception:
        h3 = False

    # ¬Q: The index of H in G is <= 4
    try:
        neg_q = h1 and isinstance(H, PermutationGroup) and H.order() > 0 and (G.order() <= 4 * H.order())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a non-trivial group",
    "H_3: H is a proper subgroup of G",
    "¬Q: The index of H in G is less than or equal to 4"
]

N_HYP = 3
NEG_Q_INDEX = 3