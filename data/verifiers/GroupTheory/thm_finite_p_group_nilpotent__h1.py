import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
    # H_1: The order of G is a power of a prime p
    try:
        order = int(witness.order())
        if order <= 0:
            h1 = False
        elif order == 1:
            h1 = True
        else:
            h1 = len(factorint(order)) == 1
    except Exception:
        h1 = False

    # neg_Q: G is not a nilpotent group
    try:
        neg_q = not bool(witness.is_nilpotent)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is a power of a prime p",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1