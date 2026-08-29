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
    def inv(g):
        return g**-1

    def comm(a, b):
        return inv(a) * inv(b) * a * b

    def conj(a, b):
        return inv(b) * a * b

    try:
        x, y, z = witness
        _ = inv(x) * y * z
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        x, y, z = witness
        
        term1_comm = comm(comm(x, inv(y)), z)
        term1 = conj(term1_comm, y)
        
        term2_comm = comm(comm(y, inv(z)), x)
        term2 = conj(term2_comm, z)
        
        term3_comm = comm(comm(z, inv(x)), y)
        term3 = conj(term3_comm, x)
        
        product = term1 * term2 * term3
        
        if hasattr(product, 'is_Identity'):
            is_id = bool(product.is_Identity)
        else:
            is_id = bool(product * x == x)
            
        neg_q_ok = not is_id
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x, y, z are elements of a group",
    "¬Q: The Hall-Witt identity fails for x, y, z"
]

N_HYP = 1
NEG_Q_INDEX = 1