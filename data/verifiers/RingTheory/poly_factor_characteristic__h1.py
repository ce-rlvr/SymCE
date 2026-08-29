import sympy
from sympy import Poly
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, n = witness
            else:
                f = witness[0]
                n = witness[1]
        else:
            f = witness
            if hasattr(f, 'domain'):
                n = f.domain.characteristic
            else:
                n = 0

        if not isinstance(f, Poly):
            f = Poly(f, x)
            
        h1 = f.is_monic
        
        if f.degree() > 0:
            char = f.domain.characteristic
        else:
            if f.is_monic:
                char = 1
            else:
                char = f.domain.characteristic
                
        neg_q = (char != n)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = ['H_1: f is a monic polynomial', '¬Q: characteristic of the factor ring is not n']

N_HYP = 1
NEG_Q_INDEX = 1