import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
from math import gcd

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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R",
    "H_3: I and J(R) are comaximal (I + J(R) = R)",
    "¬Q: I is not the entire ring R"
]

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, dict):
            if 'h1' in witness:
                h1 = bool(witness.get('h1', False))
                h2 = bool(witness.get('h2', False))
                h3 = bool(witness.get('h3', False))
                neg_q = bool(witness.get('neg_q', False))
                return [h1, h2, h3, neg_q]
            
        if hasattr(witness, 'h1'):
            h1 = bool(witness.h1)
            h2 = bool(witness.h2)
            h3 = bool(witness.h3)
            neg_q = bool(witness.neg_q)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int) and isinstance(witness[1], int):
            n, m = witness
            if n > 0:
                h1 = True
                h2 = True
                if n == 1:
                    h3 = True
                    neg_q = False
                else:
                    rad_n = 1
                    for p in factorint(n):
                        rad_n *= p
                    h3 = (gcd(m, rad_n) == 1)
                    neg_q = (gcd(m, n) != 1)
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [h1, h2, h3, neg_q]