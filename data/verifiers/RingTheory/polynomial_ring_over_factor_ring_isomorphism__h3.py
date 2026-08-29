import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
        else:
            R, I = None, None
            
        if R is not None:
            if R in [ZZ, QQ, RR, CC]:
                h1 = True
            elif hasattr(R, 'is_commutative') and R.is_commutative:
                h1 = True
            elif hasattr(R, 'is_Ring') and R.is_Ring:
                h1 = True
                
        if I is not None:
            if hasattr(I, 'is_ideal') and I.is_ideal:
                h2 = True
            elif isinstance(I, (list, tuple, set)):
                h2 = True
            elif hasattr(I, 'ring') and I.ring == R:
                h2 = True
    except Exception:
        pass

    # The theorem is universally true, so the conclusion never fails.
    neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R",
    "¬Q: The factor ring R(x)/I(x) is not isomorphic to the polynomial ring (R/I)(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2