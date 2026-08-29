import sympy
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(K, PermutationGroup)
    except Exception:
        h2_ok = False

    try:
        GH = DirectProduct(G, H)
        GHK1 = DirectProduct(GH, K)
        HK = DirectProduct(H, K)
        GHK2 = DirectProduct(G, HK)
        is_iso = GHK1.is_isomorphic(GHK2)
        neg_q_ok = not is_iso
    except Exception:
        # If the direct product cannot be formed (e.g., H is not a group),
        # then they are not isomorphic groups, so the conclusion fails.
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a group",
    "¬Q: (G x H) x K is not isomorphic to G x (H x K) or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2