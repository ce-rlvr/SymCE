import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
        G, x, y = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = h1 and (x in G)
    except Exception:
        h2 = False

    try:
        h3 = h1 and (y in G)
    except Exception:
        h3 = False

    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            x_inv = ~x
            y_inv = ~y
            is_conjugate = False
            for g in G.elements:
                if g * x_inv * ~g == y_inv:
                    is_conjugate = True
                    break
            neg_q = not is_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "¬Q: x^{-1} is not conjugate to y^{-1} in G"
]

N_HYP = 3
NEG_Q_INDEX = 3