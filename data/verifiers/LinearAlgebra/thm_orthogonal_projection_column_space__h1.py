import sympy
from sympy import eye, zeros, Matrix
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    neg_q = False
    try:
        # The witness can be either a tuple (P, Q) or just Q.
        # If just Q is provided, we compute the orthogonal projection P.
        if isinstance(witness, tuple) and len(witness) == 2:
            P, Q = witness
        else:
            Q = witness
            if hasattr(Q, 'is_Matrix') and Q.is_Matrix:
                C_list = Q.columnspace()
                if not C_list:
                    P = zeros(Q.rows, Q.rows)
                else:
                    C = C_list[0]
                    for c in C_list[1:]:
                        C = C.row_join(c)
                    P = C * (C.T * C).inv() * C.T
            else:
                return [False, False]
                
        if hasattr(P, 'is_Matrix') and P.is_Matrix and hasattr(Q, 'is_Matrix') and Q.is_Matrix:
            if P.is_square and P.rows == Q.rows:
                # H1: P is the orthogonal projection onto the column space of Q
                # 1. P is symmetric
                sym_check = (P == P.T)
                # 2. P is idempotent
                idemp_check = (P * P == P)
                # 3. Col(P) == Col(Q) -> P acts as identity on Q, and ranks match
                col_check = (P * Q == Q) and (P.rank() == Q.rank())
                
                if sym_check and idemp_check and col_check:
                    h1 = True
                    
                # ¬Q: P is not equal to the n x n identity matrix
                n = P.rows
                if P != eye(n):
                    neg_q = True
    except Exception:
        pass
    
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is the orthogonal projection matrix onto the column space of Q",
    "¬Q: P is not equal to the n x n identity matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1