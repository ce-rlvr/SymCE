import sympy
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

def conditions(witness) -> list[bool]:
    try:
        G, x, y, z = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = x in G
    except Exception:
        h1_ok = False

    try:
        h2_ok = y in G
    except Exception:
        h2_ok = False

    try:
        h3_ok = z in G
    except Exception:
        h3_ok = False

    try:
        def comm(a, b):
            return (a**-1) * (b**-1) * a * b
        
        lhs1 = comm(x, y * z)
        rhs1 = comm(x, y) * comm(x, z)
        
        lhs2 = comm(x * y, z)
        rhs2 = comm(x, z) * comm(y, z)
        
        q = (lhs1 == rhs1) and (lhs2 == rhs2)
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: y is an element of G",
    "H_3: z is an element of G",
    "¬Q: commutator identity fails"
]

N_HYP = 3
NEG_Q_INDEX = 3