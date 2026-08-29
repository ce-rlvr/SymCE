import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        is_empty = False
        
        # Direct empty checks
        if witness == sympy.EmptySet:
            is_empty = True
        elif isinstance(witness, (list, set, tuple, dict)) and len(witness) == 0:
            is_empty = True
        elif isinstance(witness, str) and witness.lower().strip() in ["empty", "emptyset", "empty_space", "empty space", "none", "0"]:
            is_empty = True
        elif witness == 0:
            is_empty = True
        elif witness is None:
            is_empty = True
            
        # Tuple (X, tau) check for topological spaces
        elif isinstance(witness, tuple) and len(witness) == 2:
            X = witness[0]
            if X == sympy.EmptySet:
                is_empty = True
            elif isinstance(X, (list, set, tuple)) and len(X) == 0:
                is_empty = True
                
        neg_q = bool(is_empty)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The suspension SX is not connected (X is the empty space)"
]

N_HYP = 0
NEG_Q_INDEX = 0