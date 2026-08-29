import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def conditions(witness):
    h1_ok = False
    try:
        if isinstance(witness, sympy.combinatorics.PermutationGroup):
            n = witness.degree
            if n < 2:
                h1_ok = (witness.order() == 1)
            else:
                h1_ok = (witness.order() == math.factorial(n) // 2)
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        if h1_ok:
            n = witness.degree
            if n in (2, 3, 6):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is the alternating group A_n",
    "¬Q: Aut(G) is not isomorphic to S_n"
]

N_HYP = 1
NEG_Q_INDEX = 1