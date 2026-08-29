import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            K = witness['K']
            L = witness['L']
        else:
            G, H, K, L = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(G.is_isomorphic(H))
    except Exception:
        h1 = False

    try:
        h2 = bool(K.is_isomorphic(L))
    except Exception:
        h2 = False

    try:
        # In sympy, the multiplication operator on PermutationGroup objects 
        # computes their direct product.
        GxK = G * K
        HxL = H * L
        neg_q = not bool(GxK.is_isomorphic(HxL))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is isomorphic to H",
    "H_2: K is isomorphic to L",
    "¬Q: The direct product G x K is not isomorphic to H x L"
]

N_HYP = 2
NEG_Q_INDEX = 2