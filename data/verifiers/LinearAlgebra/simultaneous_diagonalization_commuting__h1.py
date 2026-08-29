import sympy
from sympy import Matrix, eye, zeros
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
    try:
        if len(witness) != 2:
            return [False, False]
        A, B = witness
    except Exception:
        return [False, False]

    try:
        if not (hasattr(A, 'shape') and hasattr(B, 'shape')):
            h1 = False
        elif A.shape != B.shape or A.shape[0] != A.shape[1]:
            h1 = False
        else:
            h1 = bool(A * B == B * A)
    except Exception:
        h1 = False

    try:
        if not (hasattr(A, 'shape') and hasattr(B, 'shape')):
            neg_q = False
        elif A.shape != B.shape or A.shape[0] != A.shape[1]:
            neg_q = True
        else:
            commute = bool(A * B == B * A)
            diag_A = bool(A.is_diagonalizable())
            diag_B = bool(B.is_diagonalizable())
            sim_diag = commute and diag_A and diag_B
            neg_q = not sim_diag
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B commute (AB = BA)",
    "¬Q: A and B are not simultaneously diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1