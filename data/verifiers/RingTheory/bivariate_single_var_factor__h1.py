import sympy
from sympy import Symbol, S
from sympy.polys.domains import ZZ, QQ, RR, CC
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
    neg_q = False
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            if witness[-1] == witness[-2]:
                neg_q = True
            elif str(witness[-1]) == str(witness[-2]):
                neg_q = True
        else:
            is_ring = False
            if hasattr(witness, 'is_Ring') and witness.is_Ring:
                is_ring = True
            elif type(witness).__name__ in ('PolyRing', 'QuotientRing', 'FractionField'):
                is_ring = True
            elif witness in (ZZ, QQ, RR, CC):
                is_ring = True
            
            if not is_ring:
                neg_q = True
    except Exception:
        neg_q = True
        
    return [bool(neg_q)]

CONDITION_LABELS = ["not Q: factor ring is not isomorphic to polynomial ring"]

N_HYP = 0
NEG_Q_INDEX = 0