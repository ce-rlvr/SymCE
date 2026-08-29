import sympy
from sympy import eye, zeros
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
        A, J = witness
        h1_ok = bool(isinstance(A, MatrixBase) and A.is_square and 
                     isinstance(J, MatrixBase) and J.is_square and 
                     A.shape == J.shape)
    except Exception:
        h1_ok = False

    try:
        A, J = witness
        trace_A = A.trace()
        sum_diag_J = sum(J[i, i] for i in range(J.rows))
        det_A = A.det()
        
        prod_diag_J = 1
        for i in range(J.rows):
            prod_diag_J *= J[i, i]
            
        trace_diff = sympy.simplify(trace_A - sum_diag_J)
        det_diff = sympy.simplify(det_A - prod_diag_J)
        
        neg_q_ok = bool(trace_diff != 0 or det_diff != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over an algebraically closed field",
    "¬Q: The trace of A does not equal the sum of the diagonal entries of J, or the determinant of A does not equal the product of the diagonal entries of J"
]

N_HYP = 1
NEG_Q_INDEX = 1