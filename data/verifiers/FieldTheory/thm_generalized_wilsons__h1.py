import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings
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
    """
    Checks if the witness is a counterexample to the false conjecture:
    "The product of all non-zero elements of F is equal to -1"
    
    The witness is expected to be an integer n representing the ring Z/nZ.
    """
    try:
        n = int(witness)
        if n < 2:
            return [False]
            
        # The non-zero elements of Z/nZ are 1, 2, ..., n-1.
        # Their product modulo n is (n-1)! % n.
        prod = math.factorial(n - 1) % n
        
        # In Z/nZ, -1 is represented by n - 1.
        # The conclusion FAILS if the product is not equal to n - 1.
        neg_q = (prod != n - 1)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The product of all non-zero elements of F is not equal to -1"
]

N_HYP = 0
NEG_Q_INDEX = 0