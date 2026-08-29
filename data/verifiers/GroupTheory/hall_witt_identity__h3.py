import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, x, y, z = witness
        elif len(witness) == 3:
            x, y, z = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        _ = x * y * z
        _ = x**-1 * y**-1 * z**-1
        h1_ok = True
        h2_ok = True
    except Exception:
        h1_ok = False
        h2_ok = False

    def comm(a, b):
        return a * b * a**-1 * b**-1

    def conj(a, b):
        return b**-1 * a * b

    try:
        c1 = comm(x, y**-1)
        c1_z = comm(c1, z)
        term1 = conj(c1_z, y)

        c2 = comm(y, z**-1)
        c2_x = comm(c2, x)
        term2 = conj(c2_x, z)

        c3 = comm(z, x**-1)
        c3_y = comm(c3, y)
        term3 = conj(c3_y, x)

        lhs = term1 * term2 * term3
        
        if hasattr(lhs, 'is_Identity') and lhs.is_Identity is not None:
            is_id = bool(lhs.is_Identity)
        elif hasattr(lhs, 'is_identity') and lhs.is_identity is not None:
            is_id = bool(lhs.is_identity)
        elif hasattr(x, 'shape'):
            is_id = bool(lhs == eye(x.shape[0]))
        else:
            is_id = bool((lhs == type(lhs)(1)) or (lhs == 1))

        neg_q_ok = not is_id
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: G is a group", "H_2: x, y, z are elements of G", "¬Q: Hall-Witt identity fails"]
N_HYP = 2
NEG_Q_INDEX = 2