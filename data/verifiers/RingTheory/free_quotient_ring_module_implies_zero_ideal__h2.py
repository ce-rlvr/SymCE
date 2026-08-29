import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The quotient ring R/I is a free R-module",
    "¬Q: I is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        R, I = witness
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    try:
        h1 = False
        if R in [sympy.ZZ, sympy.QQ]:
            h1 = True
        elif hasattr(R, 'is_Ring') and getattr(R, 'is_commutative', False):
            h1 = True
    except Exception:
        h1 = False

    # H2: R/I is a free R-module
    # R/I is a free R-module if and only if I is the zero ideal (rank 1) 
    # or I is the whole ring R (rank 0, the zero module).
    try:
        is_zero_ideal = (I == 0 or I == [0] or I == (0,) or I == {0})
        is_whole_ring = (I == R or I == 1 or I == [1] or I == (1,) or I == {1})
        
        h2 = bool(is_zero_ideal or is_whole_ring)
    except Exception:
        h2 = False

    # ¬Q: I != {0}
    try:
        neg_q = not is_zero_ideal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]