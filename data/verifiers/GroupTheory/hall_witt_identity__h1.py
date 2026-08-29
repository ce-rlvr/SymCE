import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        x, y, z = witness
        _ = x * y * z
        _ = x**-1
        _ = y**-1
        _ = z**-1
        H_1_ok = True
    except Exception:
        H_1_ok = False

    try:
        def comm(a, b):
            return a**-1 * b**-1 * a * b
            
        def conj(a, b):
            return b**-1 * a * b
            
        def comm3(a, b, c):
            return comm(comm(a, b), c)
            
        t1 = conj(comm3(x, y**-1, z), y)
        t2 = conj(comm3(y, z**-1, x), z)
        t3 = conj(comm3(z, x**-1, y), x)
        
        val = t1 * t2 * t3
        
        if hasattr(val, 'is_identity'):
            is_id = bool(val.is_identity)
        else:
            is_id = bool(val * x == x)
            
        neg_Q_ok = not is_id
    except Exception:
        neg_Q_ok = False

    return [H_1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: x, y, z are elements of G",
    "¬Q: The Hall-Witt identity fails in G"
]

N_HYP = 1
NEG_Q_INDEX = 1