import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        if isinstance(witness, tuple) and len(witness) == 2:
            p, degree = witness
        else:
            p = witness.characteristic
            if callable(p): p = p()
            degree = witness.degree
            if callable(degree): degree = degree()
            
        p = int(p)
        degree = int(degree)
    except Exception:
        return [False, False, False]

    try:
        h1 = (degree >= 1)
    except Exception:
        h1 = False

    try:
        if p == 0:
            # Under the literal definition a^{p^k} in F, if p=0, a^0 = 1 in F is always true.
            # Thus any extension in char 0 is purely inseparable under this dropped-hypothesis scenario.
            h2 = True
        else:
            if not sympy.isprime(p):
                h2 = False
            else:
                h2 = False
                temp = 1
                while temp <= degree:
                    if temp == degree:
                        h2 = True
                        break
                    temp *= p
    except Exception:
        h2 = False

    try:
        neg_q = True
        if p == 0:
            if degree == 1 or degree == 0:
                neg_q = False
        else:
            temp = 1
            while temp <= degree:
                if temp == degree:
                    neg_q = False
                    break
                temp *= p
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite field extension",
    "H_2: E/F is purely inseparable",
    "not Q: The degree of E over F is not equal to p^k for any integer k >= 0"
]

N_HYP = 2
NEG_Q_INDEX = 2