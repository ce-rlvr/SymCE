import sympy
from sympy.combinatorics import (
    SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup,
    PermutationGroup, DirectProduct
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = DirectProduct(Z2, Z2)

def conditions(witness) -> list[bool]:
    try:
        G, H, K, L = witness
    except Exception:
        return [False, False, False]

    # H_1: G, H, K, and L are groups
    try:
        h1 = (isinstance(G, PermutationGroup) and
              isinstance(H, PermutationGroup) and
              isinstance(K, PermutationGroup) and
              isinstance(L, PermutationGroup))
    except Exception:
        h1 = False

    # H_2: G is isomorphic to H
    try:
        h2 = bool(G.is_isomorphic(H))
    except Exception:
        h2 = False

    # ¬Q: G \times K is NOT isomorphic to H \times L
    try:
        GxK = DirectProduct(G, K)
        HxL = DirectProduct(H, L)
        neg_q = not bool(GxK.is_isomorphic(HxL))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G, H, K, and L are groups",
    "H_2: G is isomorphic to H",
    "¬Q: G \\times K is not isomorphic to H \\times L"
]

N_HYP = 2
NEG_Q_INDEX = 2