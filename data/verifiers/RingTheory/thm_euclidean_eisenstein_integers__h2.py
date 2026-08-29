import sympy
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    h1 = False
    try:
        s = str(witness).lower().replace(" ", "")
        if "eisenstein" in s or "omega" in s or "z(w)" in s or "sqrt(-3)" in s:
            h1 = True
        elif isinstance(witness, tuple):
            h1 = True
    except Exception:
        h1 = False

    neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is the ring of Eisenstein integers Z(omega)",
    "¬Q: R is not a Euclidean domain with Euclidean function N"
]

N_HYP = 1
NEG_Q_INDEX = 1