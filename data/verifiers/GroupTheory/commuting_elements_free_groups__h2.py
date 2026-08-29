import sympy
from sympy.combinatorics import free_group
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        F, x, y = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False
        
    # H_2: xy = yx
    try:
        h2 = bool(x * y == y * x)
    except Exception:
        h2 = False
        
    # ¬Q: There do not exist z in F and integers p, q such that x = z^p and y = z^q
    try:
        in_F_x = hasattr(x, 'group') and x.group == F
        in_F_y = hasattr(y, 'group') and y.group == F
        
        if in_F_x and in_F_y:
            # In a free group, any two commuting elements are powers of a common element.
            # Thus, if they are both in F, the conclusion holds if and only if they commute.
            q_holds = bool(x * y == y * x)
        else:
            # If either is not in F, no such z in F exists.
            q_holds = False
            
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: xy = yx",
    "¬Q: There do not exist z in F and integers p, q such that x = z^p and y = z^q"
]

N_HYP = 2
NEG_Q_INDEX = 2