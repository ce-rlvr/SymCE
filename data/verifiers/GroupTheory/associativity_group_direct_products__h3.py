import sympy
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # ¬Q: The direct product (G \times H) \times K is NOT isomorphic to G \times (H \times K)
    try:
        G_H = DirectProduct(G, H)
        LHS = DirectProduct(G_H, K)
        
        H_K = DirectProduct(H, K)
        RHS = DirectProduct(G, H_K)
        
        neg_q = not LHS.is_isomorphic(RHS)
    except Exception:
        # If K is not a group, DirectProduct will fail, meaning the conclusion fails.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "¬Q: (G x H) x K is not isomorphic to G x (H x K)"
]

N_HYP = 2
NEG_Q_INDEX = 2