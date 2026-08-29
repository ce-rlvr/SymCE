import sympy
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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: H is a subgroup of G
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False

    # H_2: The index of H in G is exactly 2
    try:
        h2 = bool(G.order() == 2 * H.order())
    except Exception:
        h2 = False

    # H_3: H is an abelian group
    try:
        h3 = bool(H.is_abelian)
    except Exception:
        h3 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is exactly 2",
    "H_3: H is an abelian group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3