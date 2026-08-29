import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        if len(witness) != 4:
            return [False, False, False, False]
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
        if isinstance(n, int):
            is_int = True
        elif hasattr(n, 'is_integer'):
            if callable(n.is_integer):
                is_int = n.is_integer()
            else:
                is_int = bool(n.is_integer)
        else:
            is_int = False
            
        h2 = bool((x in F) and (y in F) and is_int)
    except Exception:
        h2 = False

    # H_3: x^n = y^n
    try:
        h3 = bool(x**n == y**n)
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
    "H_3: x^n = y^n",
    "¬Q: x != y"
]

N_HYP = 3
NEG_Q_INDEX = 3