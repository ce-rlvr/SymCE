import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) == 4:
            G, x, y, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(x in G and y in G)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isinstance(n, (int, sympy.Integer)) and n != 0 and (x**n == y**n))
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = bool(x != y)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: n is a non-zero integer such that x^n = y^n",
    "¬Q: x != y"
]

N_HYP = 2
NEG_Q_INDEX = 2