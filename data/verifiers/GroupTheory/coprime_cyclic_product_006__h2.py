import math
import sympy
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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            h1 = False
        else:
            m, n = witness
            if isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > 0 and n > 0:
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    try:
        m, n = witness
        m_int = int(m)
        n_int = int(n)
        neg_q = math.gcd(m_int, n_int) != 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: Z_m x Z_n is not isomorphic to Z_{mn}"
]

N_HYP = 1
NEG_Q_INDEX = 1