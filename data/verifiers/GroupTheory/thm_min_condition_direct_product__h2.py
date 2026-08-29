import sympy
from sympy.combinatorics import PermutationGroup
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

# Infinite cyclic group (does not satisfy the minimum condition on subgroups)
Z = sympy.S.Integers

def is_group(obj):
    if isinstance(obj, PermutationGroup):
        return True
    if obj == sympy.S.Integers or obj == "Z":
        return True
    return False

def satisfies_min(group):
    """
    Checks if a group satisfies the minimum condition on subgroups (Artinian).
    Finite groups always satisfy this condition.
    Infinite cyclic groups (like Z) do not.
    """
    if isinstance(group, PermutationGroup):
        return True
    if group == sympy.S.Integers or group == "Z":
        return False
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_group(G) and satisfies_min(G)
    except Exception:
        h1 = False
        
    try:
        if not is_group(G) or not is_group(H):
            neg_q = False
        else:
            # A direct product G x H satisfies the minimum condition on subgroups
            # if and only if BOTH G and H satisfy the minimum condition.
            g_x_h_min = satisfies_min(G) and satisfies_min(H)
            neg_q = not g_x_h_min
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G satisfies the minimum condition on subgroups",
    "¬Q: The direct product G x H does not satisfy the minimum condition on subgroups"
]

N_HYP = 1
NEG_Q_INDEX = 1