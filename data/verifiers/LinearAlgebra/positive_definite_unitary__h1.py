import sympy
from sympy import eye, zeros, Matrix, simplify
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: U is a unitary matrix
    try:
        if not getattr(witness, 'is_square', False):
            h1 = False
        else:
            n = witness.shape[0]
            diff = witness * witness.H - eye(n)
            diff_simp = diff.applyfunc(lambda val: simplify(val))
            h1 = diff_simp == zeros(n, n)
    except Exception:
        h1 = False

    # H_2: U is a positive definite matrix
    try:
        h2 = False
        if hasattr(witness, 'is_positive_definite') and witness.is_positive_definite == True:
            h2 = True
        elif hasattr(witness, 'H'):
            # For non-Hermitian/non-symmetric matrices, check if the Hermitian part is positive definite
            H = (witness + witness.H) / 2
            if hasattr(H, 'is_positive_definite') and H.is_positive_definite == True:
                h2 = True
            else:
                # Fallback: check if all eigenvalues of the Hermitian part are strictly positive
                evals = H.eigenvals()
                all_pos = True
                for e in evals:
                    if hasattr(e, 'is_positive') and e.is_positive == True:
                        continue
                    e_simp = simplify(e)
                    if hasattr(e_simp, 'is_positive') and e_simp.is_positive == True:
                        continue
                    try:
                        if float(e_simp.evalf()) > 0:
                            continue
                    except Exception:
                        pass
                    all_pos = False
                    break
                if all_pos and len(evals) > 0:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: U is not the n x n identity matrix
    try:
        if not getattr(witness, 'is_square', False):
            neg_q = False
        else:
            n = witness.shape[0]
            diff = witness - eye(n)
            diff_simp = diff.applyfunc(lambda val: simplify(val))
            neg_q = diff_simp != zeros(n, n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "H_2: U is a positive definite matrix",
    "¬Q: U is not the n x n identity matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2