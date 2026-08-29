import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import free_group
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

F1, a = free_group("a")
F2, f2a, f2b = free_group("a, b")
F3, f3a, f3b, f3c = free_group("a, b, c")

def conditions(witness) -> list[bool]:
    try:
        F, x, y, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # H_2: x and y are elements of F
    try:
        h2 = hasattr(x, 'group') and x.group == F and hasattr(y, 'group') and y.group == F
    except Exception:
        try:
            h2 = (x in F) and (y in F)
        except Exception:
            h2 = False

    # H_3: n is a non-zero integer
    try:
        h3 = isinstance(n, (int, sympy.Integer)) and int(n) != 0
    except Exception:
        h3 = False

    # ¬Q: x != y
    try:
        neg_q = bool(x != y)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: x and y are elements of F",
    "H_3: n is a non-zero integer",
    "¬Q: x != y"
]

N_HYP = 3
NEG_Q_INDEX = 3