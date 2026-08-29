import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        q, n = witness
    except Exception:
        return [False, False]
        
    try:
        if isinstance(q, int) and q >= 2:
            f = factorint(q)
            h1 = (len(f) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    try:
        # The conclusion states that there exists a normal basis for F_{q^n} over F_q.
        # By the Normal Basis Theorem, this is true if and only if n is a positive integer.
        # If n is not a positive integer (e.g., n <= 0 or n is a fraction), 
        # F_{q^n} is not a valid field extension of degree n, and the conclusion fails.
        if isinstance(n, int) and n >= 1:
            q_holds = True
        else:
            q_holds = False
            
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field (q is a prime power)",
    "¬Q: The set does not form a basis for F_{q^n} over F_q (e.g., n is not a positive integer)"
]

N_HYP = 1
NEG_Q_INDEX = 1