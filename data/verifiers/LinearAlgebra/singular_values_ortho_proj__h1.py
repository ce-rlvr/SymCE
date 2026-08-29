import sympy
from sympy import Matrix, eye, zeros, simplify
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    try:
        # H_1: P is a square matrix
        P = Matrix(witness)
        h1 = P.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # The singular values of P are exactly k ones and n-k zeros
            # if and only if P^H P is an orthogonal projection (idempotent).
            # Since P^H P is always Hermitian, it is diagonalizable, and its
            # eigenvalues are exactly k ones and n-k zeros iff (P^H P)^2 == P^H P.
            P_H_P = P.H * P
            diff = P_H_P**2 - P_H_P
            
            q = True
            for i in range(P.rows):
                for j in range(P.cols):
                    val = simplify(diff[i, j])
                    if val != 0 and val.is_zero is not True:
                        q = False
                        break
                if not q:
                    break
            
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a square matrix",
    "¬Q: The singular values of P do not consist of exactly k ones and n-k zeros"
]

N_HYP = 1
NEG_Q_INDEX = 1