import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

    # H_2: H is a solvable group
    try:
        h2 = bool(H.is_solvable)
    except Exception:
        h2 = False

    # ¬Q: G x H is not a solvable group
    try:
        try:
            # In sympy, the * operator on PermutationGroup computes the direct product
            GxH = G * H
            neg_q = not bool(GxH.is_solvable)
        except Exception:
            # Fallback: G x H is solvable iff both G and H are solvable
            neg_q = not (bool(G.is_solvable) and bool(H.is_solvable))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: H is a solvable group",
    "¬Q: G x H is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2