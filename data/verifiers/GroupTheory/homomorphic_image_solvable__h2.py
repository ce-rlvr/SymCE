import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a solvable group
    try:
        if not isinstance(G, PermutationGroup):
            h2 = False
        else:
            solvable_G = G.is_solvable
            if callable(solvable_G):
                h2 = bool(solvable_G())
            else:
                h2 = bool(solvable_G)
    except Exception:
        h2 = False

    # ¬Q: H is not a solvable group
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            solvable_H = H.is_solvable
            if callable(solvable_H):
                neg_q = not bool(solvable_H())
            else:
                neg_q = not bool(solvable_H)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is a solvable group",
    "¬Q: H is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2