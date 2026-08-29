import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

try:
    from sympy.combinatorics.free_groups import free_group
    F2, _ = free_group("x y")
    F1, _ = free_group("x")
except Exception:
    F2 = "F2"
    F1 = "Z"

def is_group(G):
    from sympy.combinatorics import PermutationGroup
    if isinstance(G, PermutationGroup):
        return True
    if type(G).__name__ in ('FreeGroup', 'FpGroup'):
        return True
    if isinstance(G, str) and G in ["Z", "F2", "F_2", "Q", "R", "C", "Z x Z"]:
        return True
    return False

def satisfies_acc_normal(G):
    from sympy.combinatorics import PermutationGroup
    if isinstance(G, PermutationGroup):
        return True
    if type(G).__name__ == 'FreeGroup':
        if len(G.generators) <= 1:
            return True
        else:
            return False
    if type(G).__name__ == 'FpGroup':
        try:
            if G.order() != sympy.oo:
                return True
        except Exception:
            pass
        return False
    if isinstance(G, str):
        if G in ["Z", "Z1", "trivial", "Z x Z"]:
            return True
        if G in ["F2", "F_2", "F3", "F_3", "Q", "R", "C"]:
            return False
    raise ValueError("Unknown group type")

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups
    try:
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False
        
    # H_2: G satisfies the ascending chain condition on normal subgroups
    try:
        h2 = satisfies_acc_normal(G)
    except Exception:
        h2 = False
        
    # ¬Q: H does not satisfy the ascending chain condition on normal subgroups
    try:
        neg_q = not satisfies_acc_normal(H)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G satisfies the ascending chain condition on normal subgroups",
    "¬Q: H does not satisfy the ascending chain condition on normal subgroups"
]

N_HYP = 2
NEG_Q_INDEX = 2