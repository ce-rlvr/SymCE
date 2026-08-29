import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple (F, x) where F is a free group and x is an element of F.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, x = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: F is a free group and x is an element of F
    try:
        h1 = (type(F).__name__ == 'FreeGroup' and 
              type(x).__name__ == 'FreeGroupElement' and 
              x.group == F)
    except Exception:
        h1 = False
        
    # ¬Q: The centralizer of x in F is NOT an infinite cyclic group
    try:
        if not h1:
            neg_q = False
        else:
            # In a free group F, the centralizer of x is infinite cyclic UNLESS
            # x is the identity element and F is not of rank 1.
            # If x == e, C_F(e) = F. F is infinite cyclic iff F has exactly 1 generator.
            # If x != e, C_F(x) is always infinite cyclic.
            is_infinite_cyclic = (x != F.identity) or (len(F.generators) == 1)
            neg_q = not is_infinite_cyclic
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group and x is an element of F",
    "¬Q: The centralizer of x in F is not an infinite cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1