import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
F, a, b = free_group("a, b")
FreeGroupType = type(F)

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

def conditions(witness):
    try:
        F_obj, x, y = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a free group
    try:
        h1 = isinstance(F_obj, FreeGroupType)
    except Exception:
        h1 = False
        
    # H_2: x and y are elements of F
    try:
        h2 = (getattr(x, 'group', None) == F_obj) and (getattr(y, 'group', None) == F_obj)
        if not h2:
            try:
                h2 = (x in F_obj) and (y in F_obj)
            except Exception:
                pass
    except Exception:
        h2 = False
        
    # neg_Q: There does NOT exist z in F and integers p, q such that x = z^p and y = z^q
    # In a free group, two elements are powers of a common element
    # if and only if they commute. Thus, the conclusion fails iff they do not commute.
    try:
        neg_q = bool(x * y != y * x)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: x and y are elements of F",
    "¬Q: There do not exist z in F and integers p, q such that x = z^p and y = z^q"
]

N_HYP = 2
NEG_Q_INDEX = 2