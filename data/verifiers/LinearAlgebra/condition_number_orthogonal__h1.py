import sympy
from sympy import eye, zeros, simplify, Matrix, I
from sympy.abc import x, y, z
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: Q is an orthogonal matrix
        # An orthogonal matrix is a square matrix Q such that Q^T * Q = I
        if not hasattr(witness, 'rows') or not hasattr(witness, 'cols') or witness.rows != witness.cols:
            h1 = False
        else:
            n = witness.rows
            diff = witness.T * witness - eye(n)
            h1 = all(simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
    except Exception:
        h1 = False

    try:
        # ¬Q: The condition number of Q with respect to the 2-norm is not equal to 1
        # The 2-norm condition number is the ratio of the largest to smallest singular value.
        # Singular values are the square roots of the eigenvalues of Q^H * Q.
        if not hasattr(witness, 'rows') or not hasattr(witness, 'cols') or witness.rows != witness.cols:
            neg_q = False
        else:
            n = witness.rows
            if n == 0:
                neg_q = False
            else:
                M = witness.H * witness
                evals = list(M.eigenvals().keys())
                
                try:
                    # Attempt numerical evaluation
                    evals_num = [abs(complex(e.evalf())) for e in evals]
                    min_val = min(evals_num)
                    max_val = max(evals_num)
                    if min_val < 1e-12:
                        # Matrix is singular, condition number is infinity
                        neg_q = True
                    else:
                        # Condition number squared
                        cond_num_sq = max_val / min_val
                        neg_q = cond_num_sq > 1.000001
                except Exception:
                    # Fallback to symbolic comparison if numerical evaluation fails
                    unique_evals = []
                    for e in evals:
                        e_simp = simplify(e)
                        if not any(simplify(e_simp - ue) == 0 for ue in unique_evals):
                            unique_evals.append(e_simp)
                    # If there is more than one unique eigenvalue, the condition number is not 1
                    neg_q = len(unique_evals) > 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "¬Q: The condition number of Q with respect to the 2-norm is not equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1