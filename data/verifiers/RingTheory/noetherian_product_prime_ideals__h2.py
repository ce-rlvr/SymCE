import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import ZZ, QQ
from sympy.abc import x, y, z

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

def conditions(witness):
    try:
        R, I = witness
    except Exception:
        return [False, False]
        
    # H1: R is a commutative Noetherian ring
    try:
        h1 = False
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative and hasattr(R, 'is_noetherian') and R.is_noetherian:
            h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: The conclusion fails
    try:
        neg_q = False
        if h1 and R in (ZZ, QQ):
            if isinstance(I, (set, list, tuple)):
                I_set = set(I)
                if all(isinstance(elem, (int, sympy.Integer, sympy.Rational, float)) for elem in I_set):
                    # In ZZ or QQ, the only finite ideal is {0}.
                    # If I is a finite set other than {0}, no product of prime ideals 
                    # containing I can be contained in I, because such a product would 
                    # either be infinite or {0}. If it is {0}, then one of the prime 
                    # ideals must be (0), which means (0) contains I, so I must be 
                    # a subset of {0}. Since I != {0}, this is impossible.
                    if I_set == {0} or I_set == {sympy.Integer(0)} or I_set == {sympy.Rational(0)}:
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: There do not exist prime ideals P_1, ..., P_n containing I such that P_1 ... P_n is contained in I"
]

N_HYP = 1
NEG_Q_INDEX = 1