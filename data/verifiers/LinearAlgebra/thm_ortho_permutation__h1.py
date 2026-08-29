import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Matrix
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = False
        if hasattr(witness, 'is_square') and witness.is_square:
            is_perm = True
            for i in range(witness.rows):
                row_sum = 0
                for j in range(witness.cols):
                    val = witness[i, j]
                    if val not in (0, 1):
                        is_perm = False
                        break
                    row_sum += val
                if not is_perm or row_sum != 1:
                    is_perm = False
                    break
            if is_perm:
                for j in range(witness.cols):
                    col_sum = 0
                    for i in range(witness.rows):
                        col_sum += witness[i, j]
                    if col_sum != 1:
                        is_perm = False
                        break
            h1 = is_perm
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_square') and witness.is_square:
            I = eye(witness.rows)
            is_ortho = (witness.T * witness == I)
            neg_q = not is_ortho
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a permutation matrix",
    "¬Q: P is not an orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1