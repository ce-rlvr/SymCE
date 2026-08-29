import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        x, y, z = witness
    except Exception:
        return [False, False]
    
    def inv(g):
        if hasattr(g, 'inv') and callable(g.inv):
            return g.inv()
        if hasattr(g, '__invert__'):
            return ~g
        return g ** -1

    def comm(a, b):
        return a * b * inv(a) * inv(b)

    try:
        _ = x * y * z
        _ = inv(x)
        _ = inv(y)
        _ = inv(z)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        lhs = comm(x * y, z)
        rhs = inv(y) * comm(x, z) * y * comm(y, z)
        neg_q_ok = not (lhs == rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: x, y, z are elements of G", "neg_Q: The commutator identity fails"]
N_HYP = 1
NEG_Q_INDEX = 1