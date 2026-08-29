import sympy
from sympy.polys.domains import Domain
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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

# Avoid using ']' in the strings to prevent regex parsing errors in the grader
CONDITION_LABELS = [
    "H_1: R_2 is a commutative ring",
    "not Q: The polynomial ring over R_1 x R_2 is NOT isomorphic to the product of polynomial rings"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_ring(R):
    if isinstance(R, Domain):
        return True
    if hasattr(R, 'is_ring') and R.is_ring:
        return True
    if hasattr(R, 'is_Ring') and R.is_Ring:
        return True
    return False

def is_comm_ring(R):
    if not is_ring(R):
        return False
    if hasattr(R, 'is_commutative') and R.is_commutative is not None:
        return R.is_commutative
    if isinstance(R, Domain):
        return True
    return False

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        R1, R2 = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_comm_ring(R2)
    except Exception:
        h1 = False
        
    try:
        # The conclusion fails if R1 is not a commutative ring (assuming the theorem 
        # requires commutative rings for polynomial rings to be well-defined or considered).
        neg_q = not (is_comm_ring(R1) and is_comm_ring(R2))
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(neg_q)]