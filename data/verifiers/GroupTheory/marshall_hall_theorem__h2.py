import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

F2 = free_group("a, b")
F3 = free_group("x, y, z")
FreeGroupType = type(F2)

class CommutatorSubgroup:
    """Represents the commutator subgroup [G, G] of a group G."""
    def __init__(self, group):
        self.group = group

def is_finitely_generated(H):
    if isinstance(H, CommutatorSubgroup):
        if isinstance(H.group, FreeGroupType):
            # The commutator subgroup of a free group is finitely generated iff rank <= 1
            return len(H.group.generators) <= 1
    if hasattr(H, "is_finitely_generated"):
        return H.is_finitely_generated()
    if isinstance(H, (list, tuple, set)):
        return True
    if isinstance(H, FreeGroupType):
        return True
    return True

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: There does not exist a subgroup K of finite index in F such that H is a free factor of K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        F, H = witness
    except Exception:
        return [False, False]
        
    # H_1: F is a free group
    try:
        h1 = isinstance(F, FreeGroupType)
    except Exception:
        h1 = False
        
    # ¬Q: There does not exist a subgroup K of finite index in F such that H is a free factor of K
    try:
        if not h1:
            neg_q = False
        else:
            is_subgroup = False
            if isinstance(H, CommutatorSubgroup) and H.group == F:
                is_subgroup = True
            elif H == F:
                is_subgroup = True
            elif isinstance(H, (list, tuple, set)):
                is_subgroup = all(hasattr(g, 'group') and g.group == F for g in H)
            elif hasattr(H, "is_subgroup"):
                is_subgroup = H.is_subgroup(F)
                
            if not is_subgroup:
                neg_q = False
            else:
                # By Marshall Hall's Theorem and Schreier's Lemma, for a finitely generated free group F,
                # H is a free factor of a finite index subgroup K iff H is finitely generated.
                neg_q = not is_finitely_generated(H)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]