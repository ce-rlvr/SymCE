import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # H1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H2: The order of G is 2p^2
    try:
        if h1:
            order = int(witness.order())
            if order % 2 == 0:
                half_order = order // 2
                root = int(math.isqrt(half_order))
                h2 = bool((root * root == half_order) and (root > 0))
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        if h1:
            neg_q = not bool(witness.is_solvable)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is 2p^2",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2