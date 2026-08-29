import sympy
import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        p = int(witness)
        if p < 2:
            return [False]
    except Exception:
        return [False]
        
    try:
        product = 1
        for x in range(1, p):
            # x is not congruent to its inverse mod p if and only if x^2 != 1 mod p.
            # This correctly includes non-invertible elements, for which an inverse does not exist.
            if (x * x) % p != 1:
                product = (product * x) % p
        
        neg_q = (product % p != 1)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The product of all x in {1..p-1} with x^2 != 1 mod p is not congruent to 1 mod p"
]

N_HYP = 0
NEG_Q_INDEX = 0