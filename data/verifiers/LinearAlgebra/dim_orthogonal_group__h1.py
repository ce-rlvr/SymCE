import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        n = witness
        # The conclusion is that O(n) is a smooth manifold of dimension n(n-1)/2.
        # This is true when n is a non-negative integer.
        # For other values (e.g., negative integers, fractions, etc.), O(n) is either
        # undefined or not a smooth manifold of the given dimension.
        if isinstance(n, (int, sympy.Integer)) and n >= 0:
            q = True
        else:
            q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: O(n) is not a smooth manifold of dimension n(n-1)/2"
]

N_HYP = 0
NEG_Q_INDEX = 0