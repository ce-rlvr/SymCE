import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, x, y = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x and y are conjugate in G
    try:
        if not h1:
            h2 = False
        elif not (isinstance(x, Permutation) and isinstance(y, Permutation)):
            h2 = False
        elif not (G.contains(x) and G.contains(y)):
            h2 = False
        elif G.order() > 5000:
            h2 = False
        else:
            h2 = any(g * x * ~g == y for g in G.elements)
    except Exception:
        h2 = False

    # ¬Q: x^{-1} and y^{-1} are NOT conjugate in G
    try:
        if not h1:
            neg_q = False
        elif not (isinstance(x, Permutation) and isinstance(y, Permutation)):
            neg_q = False
        elif not (G.contains(x) and G.contains(y)):
            neg_q = False
        elif G.order() > 5000:
            neg_q = False
        else:
            x_inv = ~x
            y_inv = ~y
            are_conjugate = any(g * x_inv * ~g == y_inv for g in G.elements)
            neg_q = not are_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are conjugate in G",
    "¬Q: x^{-1} and y^{-1} are not conjugate in G"
]

N_HYP = 2
NEG_Q_INDEX = 2