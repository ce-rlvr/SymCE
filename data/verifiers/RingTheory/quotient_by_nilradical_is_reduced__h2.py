import sympy
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

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

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, N = witness
        else:
            R = sympy.ZZ
            N = witness
            
        if R == sympy.ZZ:
            h1 = True
            try:
                n = abs(int(N))
                if n == 0 or n == 1:
                    neg_q = False
                else:
                    factors = factorint(n)
                    is_sq_free = all(v == 1 for v in factors.values())
                    neg_q = not is_sq_free
            except (ValueError, TypeError):
                pass
        else:
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            elif hasattr(R, 'is_Commutative'):
                h1 = bool(R.is_Commutative)
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The nilradical of the quotient ring R/N is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1