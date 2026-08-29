import sympy
from sympy import QQ, RR, CC, ZZ, GF
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

CONDITION_LABELS = [
    r"¬Q: The multiplicative group F^\times of non-zero elements of F is not a cyclic group"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        # The conclusion states that the non-zero elements of F form a cyclic group under multiplication.
        # This is true if and only if F is a finite field.
        # If F is an infinite field (like QQ, RR, CC), its multiplicative group is not cyclic.
        # If F is not a field, its non-zero elements do not form a group under multiplication.
        if getattr(witness, 'is_FiniteField', False):
            q_holds = True
        else:
            q_holds = False
            
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [neg_q]