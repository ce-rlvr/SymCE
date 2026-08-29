import sympy
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

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # H_1: Let U be an n × n complex matrix.
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.rows == witness.cols and witness.rows > 0
    except Exception:
        h1 = False

    # ¬Q: Not all singular values of U are exactly equal to 1.
    # Mathematically, all singular values of a square matrix U are 1 
    # if and only if U is unitary (i.e., U^H * U = I).
    try:
        if not (isinstance(witness, sympy.MatrixBase) and witness.rows == witness.cols and witness.rows > 0):
            neg_q = False
        else:
            n = witness.rows
            diff = witness.H * witness - sympy.eye(n)
            # Check if U^H * U is exactly the identity matrix
            is_unitary = all(sympy.simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
            neg_q = not is_unitary
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "¬Q: Not all singular values of U are exactly equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1