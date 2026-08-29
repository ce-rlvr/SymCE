import sympy
import sympy.ntheory
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
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

CONDITION_LABELS = [
    "H_1: p != 5",
    "¬Q: The equivalence (-5/p) = 1 iff p = 1, 3, 7, 9 (mod 20) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        p = int(witness)
    except Exception:
        return [False, False]
    
    try:
        h1 = (p != 5)
    except Exception:
        h1 = False
        
    try:
        # Evaluate the Legendre symbol (-5 / p)
        # If p is not prime, legendre_symbol raises ValueError.
        # We catch it and treat the symbol as undefined (so equality to 1 is False).
        val = sympy.ntheory.legendre_symbol(-5, p)
        lhs = (val == 1)
    except Exception:
        lhs = False
        
    try:
        rhs = (p % 20 in [1, 3, 7, 9])
    except Exception:
        rhs = False
        
    try:
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]