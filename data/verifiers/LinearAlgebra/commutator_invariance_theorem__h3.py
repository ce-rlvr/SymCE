import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            A, B, W = witness
        elif len(witness) == 4:
            V, A, B, W = witness
        else:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    # H1: V is a vector space
    try:
        if not isinstance(W, Matrix):
            W_list = list(W)
            if len(W_list) == 0:
                W_mat = zeros(A.shape[0], 1)
            elif all(isinstance(v, Matrix) for v in W_list):
                W_mat = sympy.Matrix.hstack(*W_list)
            elif all(isinstance(v, list) for v in W_list):
                W_mat = Matrix(W_list).T
            else:
                W_mat = Matrix(W_list)
        else:
            W_mat = W
            
        h1 = (isinstance(A, Matrix) and isinstance(B, Matrix) and 
              A.is_square and B.is_square and A.shape == B.shape and 
              W_mat.shape[0] == A.shape[0])
    except Exception:
        h1 = False

    # H2: A and B are linear operators on V
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H3: W is an A-invariant subspace
    try:
        if h1:
            rank_W = W_mat.rank()
            h3 = (W_mat.row_join(A * W_mat).rank() == rank_W)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: W is a B-invariant subspace
    try:
        if h1:
            rank_W = W_mat.rank()
            h4 = (W_mat.row_join(B * W_mat).rank() == rank_W)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: W is not invariant under the commutator operator AB - BA
    try:
        if h1:
            Comm = A * B - B * A
            rank_W = W_mat.rank()
            neg_q = (W_mat.row_join(Comm * W_mat).rank() > rank_W)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: A and B are linear operators on V",
    "H_3: W is an A-invariant subspace",
    "H_4: W is a B-invariant subspace",
    "¬Q: W is not invariant under the commutator operator AB - BA"
]

N_HYP = 4
NEG_Q_INDEX = 4