import sympy
from sympy.matrices import MatrixBase
from sympy import Matrix, eye, simplify, zeros
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: Q is an n x n real orthogonal matrix
    h1_ok = False
    try:
        if isinstance(witness, MatrixBase) and witness.is_square:
            is_real = True
            for val in witness:
                if val.is_real is False or val.has(sympy.I):
                    is_real = False
                    break
            if is_real:
                n = witness.shape[0]
                diff = witness.T * witness - eye(n)
                if all(simplify(val) == 0 for val in diff):
                    h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The null space of Q - I is not the orthogonal complement of the column space of Q - I
    neg_q_ok = False
    try:
        if isinstance(witness, MatrixBase) and witness.is_square:
            n = witness.shape[0]
            A = witness - eye(n)
            
            # The orthogonal complement of Col(A) is Null(A^T).
            # We check if Null(A) == Null(A^T).
            # Since A is square, dim(Null(A)) == dim(Null(A^T)).
            # Thus, they are equal if and only if Null(A) is a subset of Null(A^T).
            N1 = A.nullspace()
            
            is_same = True
            for v in N1:
                prod = A.T * v
                if not all(simplify(x) == 0 for x in prod):
                    is_same = False
                    break
            
            neg_q_ok = not is_same
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Q is an n x n real orthogonal matrix",
    "¬Q: The null space of Q - I is not the orthogonal complement of the column space of Q - I"
]

N_HYP = 1
NEG_Q_INDEX = 1