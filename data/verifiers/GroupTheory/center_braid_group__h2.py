import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "¬Q: The center of B_n is not an infinite cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    n = witness
    
    try:
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False
        
    try:
        if not isinstance(n, int):
            neg_q = False
        else:
            # Mathematically, the center of the braid group B_n is infinite cyclic for all n >= 2.
            # For n = 1, B_1 is the trivial group, so its center is trivial (finite).
            # The literal conclusion "The center of B_n is an infinite cyclic group" 
            # is mathematically true for all n >= 2.
            # Thus, its negation is True iff n < 2.
            is_infinite_cyclic = (n >= 2)
            neg_q = not is_infinite_cyclic
    except Exception:
        neg_q = False
        
    return [h1, neg_q]