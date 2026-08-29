import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

try:
    from sympy.combinatorics import free_group
    F2 = free_group("x y")[0]
    F3 = free_group("x y z")[0]
    Z_group = free_group("x")[0]
except ImportError:
    pass

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

def has_finite_prufer_rank(grp):
    if isinstance(grp, PermutationGroup):
        return True
    if type(grp).__name__ == 'FreeGroup':
        return len(grp.generators) <= 1
    raise ValueError("Cannot determine Prufer rank for this object")

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        h1_ok = bool(has_finite_prufer_rank(H))
    except Exception:
        h1_ok = False
        
    try:
        q = has_finite_prufer_rank(G) and has_finite_prufer_rank(H)
        neg_q_ok = not bool(q)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a group of finite Prufer rank",
    "¬Q: G x H does not have finite Prufer rank"
]

N_HYP = 1
NEG_Q_INDEX = 1
