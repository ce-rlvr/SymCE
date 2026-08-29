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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        Q, lmbda = witness
    except Exception:
        return [False, False, False]
    
    # H1: Q is an orthogonal matrix, satisfying Q^T Q = I
    try:
        if not isinstance(Q, sympy.MatrixBase):
            Q = sympy.Matrix(Q)
        n, m = Q.shape
        if n != m:
            h1 = False
        else:
            diff = Q.T * Q - sympy.eye(n)
            if diff.is_zero_matrix:
                h1 = True
            else:
                h1 = sympy.simplify(diff).is_zero_matrix == True
    except Exception:
        h1 = False

    # H2: lambda is a real root of the characteristic polynomial of Q
    try:
        lmbda = sympy.sympify(lmbda)
        is_real = False
        if lmbda.is_real:
            is_real = True
        elif sympy.simplify(sympy.im(lmbda)) == 0:
            is_real = True
            
        if not is_real:
            h2 = False
        else:
            n = Q.shape[0]
            char_matrix = Q - lmbda * sympy.eye(n)
            det_val = char_matrix.det()
            if det_val == 0:
                h2 = True
            else:
                h2 = (sympy.simplify(det_val) == 0)
    except Exception:
        h2 = False

    # neg_Q: lambda not in {1, -1}
    try:
        lmbda = sympy.sympify(lmbda)
        if sympy.simplify(lmbda - 1) == 0 or sympy.simplify(lmbda + 1) == 0:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix, satisfying Q^T Q = I",
    "H_2: lambda is a real root of the characteristic polynomial of Q",
    "¬Q: lambda is not in {1, -1}"
]

N_HYP = 2
NEG_Q_INDEX = 2