import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

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

def conditions(witness):
    try:
        d = int(witness)
        h1 = (d > 1) and bool(sympy.is_squarefree(d))
    except Exception:
        h1 = False

    try:
        d = int(witness)
        if d <= 0:
            neg_q = True
        else:
            root = math.isqrt(d)
            if root * root == d:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d > 1 is a squarefree integer",
    "¬Q: The group of units of Z adjoin sqrt(d) is not isomorphic to Z/2Z x Z"
]

N_HYP = 1
NEG_Q_INDEX = 1