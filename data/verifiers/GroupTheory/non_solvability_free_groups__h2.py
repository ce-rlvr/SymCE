import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import free_group
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

try:
    F1, _ = free_group("x")
    F2, _ = free_group("x, y")
except Exception:
    F1 = None
    F2 = None

def conditions(witness) -> list[bool]:
    # H_1: F is a free group
    try:
        h1 = False
        if type(witness).__name__ == 'FreeGroup':
            h1 = True
        elif type(witness).__name__ == 'FpGroup' and len(witness.relators) == 0:
            h1 = True
        elif hasattr(witness, 'order'):
            order = witness.order() if callable(witness.order) else witness.order
            if order == 1:
                h1 = True
    except Exception:
        h1 = False

    # ¬Q: F is a solvable group
    try:
        neg_q = False
        if type(witness).__name__ == 'FreeGroup':
            neg_q = len(witness.generators) <= 1
        elif type(witness).__name__ == 'FpGroup' and len(witness.relators) == 0:
            neg_q = len(witness.generators) <= 1
        elif hasattr(witness, 'is_solvable'):
            val = witness.is_solvable
            neg_q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'order'):
            order = witness.order() if callable(witness.order) else witness.order
            if order == 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: F is a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1