import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(A, MatrixBase) and isinstance(B, MatrixBase) and A.is_square and B.is_square
    except Exception:
        h1 = False

    try:
        h2 = bool(B.is_diagonalizable())
    except Exception:
        h2 = False

    try:
        m, n = A.shape
        p, q = B.shape
        K = Matrix(m*p, n*q, lambda i, j: A[i//p, j//q] * B[i%p, j%q])
        neg_q = not bool(K.is_diagonalizable())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are square matrices",
    "H_2: B is diagonalizable",
    "¬Q: A \otimes B is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2