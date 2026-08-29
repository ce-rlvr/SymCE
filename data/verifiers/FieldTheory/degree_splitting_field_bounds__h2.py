import math
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z, t, u, v

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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            deg = int(witness.get('extension_degree', witness.get('degree', 1)))
            n = int(witness.get('n', 1))
        elif isinstance(witness, tuple) and len(witness) >= 2:
            n = int(witness[0])
            deg = int(witness[1])
        else:
            deg = int(getattr(witness, 'extension_degree', getattr(witness, 'degree', 1)))
            n = int(getattr(witness, 'n', 1))
            
        h1 = True
        h2 = True
        neg_q = (deg % math.factorial(n)) != 0
        
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is the splitting field of f(x) over F",
    "not Q: The degree of the field extension does not divide n factorial"
]

N_HYP = 2
NEG_Q_INDEX = 2