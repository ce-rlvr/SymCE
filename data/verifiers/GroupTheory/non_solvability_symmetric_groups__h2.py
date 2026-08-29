import sympy
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

def conditions(witness) -> list[bool]:
    # H_1: n is an integer such that n >= 5
    try:
        n = int(witness)
        h1 = (n == witness) and (n >= 5)
    except Exception:
        h1 = False

    # ¬Q: The group S_n is solvable
    try:
        n = int(witness)
        if n > 0:
            neg_q = bool(SymmetricGroup(n).is_solvable)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 5",
    "¬Q: The group S_n is solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1