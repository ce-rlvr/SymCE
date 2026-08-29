import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

class InfiniteGroup:
    def __init__(self, name, fg):
        self.name = name
        self.fg = fg

class InfiniteSubgroup:
    def __init__(self, name, group, fg):
        self.name = name
        self.group = group
        self.fg = fg

# Setup named objects for the witness to use
F2 = InfiniteGroup("F2", True)
F2_commutator = InfiniteSubgroup("F2_commutator", F2, False)

Z_wr_Z = InfiniteGroup("Z_wr_Z", True)
Z_wr_Z_base = InfiniteSubgroup("Z_wr_Z_base", Z_wr_Z, False)

BS_1_2 = InfiniteGroup("BS(1, 2)", True)
BS_1_2_kernel = InfiniteSubgroup("Kernel of BS(1, 2) -> Z", BS_1_2, False)

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

def is_finitely_generated(obj):
    if isinstance(obj, InfiniteGroup) or isinstance(obj, InfiniteSubgroup):
        return obj.fg
    if hasattr(obj, 'generators'):
        return True
    return False

def is_subgroup(H, G):
    if isinstance(H, InfiniteSubgroup):
        return H.group == G
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    try:
        if hasattr(H, 'generators'):
            return all(g in G for g in H.generators)
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = bool(is_finitely_generated(G))
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = bool(is_subgroup(H, G))
    except Exception:
        h2_ok = False
        
    try:
        neg_q_ok = not is_finitely_generated(H)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is finitely generated",
    "H_2: H is a subgroup of G",
    "¬Q: H is not a finitely generated group"
]

N_HYP = 2
NEG_Q_INDEX = 2