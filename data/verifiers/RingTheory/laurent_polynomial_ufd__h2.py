import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import ZZ, QQ

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
    try:
        h1 = bool(witness.is_UFD)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'laurent_ring_is_UFD'):
            val = witness.laurent_ring_is_UFD
            if callable(val):
                val = val()
            neg_q = not bool(val)
        elif hasattr(witness, 'is_laurent_UFD'):
            val = witness.is_laurent_UFD
            if callable(val):
                val = val()
            neg_q = not bool(val)
        else:
            neg_q = not bool(witness.is_UFD)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "not Q: The ring of Laurent polynomials over R is not a Unique Factorization Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1