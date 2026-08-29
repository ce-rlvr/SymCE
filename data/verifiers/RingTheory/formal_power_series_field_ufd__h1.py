import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import z3
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The formal power series ring is not a unique factorization domain"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F', witness)
            n = witness.get('n', 1)
        elif isinstance(witness, tuple) and len(witness) == 2:
            F, n = witness
        else:
            F = witness
            n = 1
    except Exception:
        F = witness
        n = 1

    try:
        if isinstance(n, int):
            h1 = n > 0
        elif hasattr(n, 'is_Integer') and n.is_Integer:
            h1 = int(n) > 0
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(F, int) or (hasattr(F, 'is_Integer') and F.is_Integer):
            is_ufd_F = isprime(int(F))
        elif hasattr(F, 'is_UFD'):
            is_ufd_F = bool(F.is_UFD)
        elif hasattr(F, 'is_Field') and F.is_Field:
            is_ufd_F = True
        else:
            is_ufd_F = False
            
        neg_q = not is_ufd_F
    except Exception:
        neg_q = False

    return [h1, neg_q]