import sympy
from sympy import Matrix, eye, zeros, I
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: A is an n x n complex matrix
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H2: A is Hermitian
    try:
        h2 = bool(witness == witness.H)
    except Exception:
        h2 = False

    # neg_Q: Not all eigenvalues of A are strictly positive real numbers
    try:
        eigenvals = witness.eigenvals()
        all_positive_real = True
        for val in eigenvals.keys():
            val = sympy.simplify(val)
            try:
                if val.is_real:
                    if not bool(val > 0):
                        all_positive_real = False
                        break
                else:
                    c_val = complex(val.evalf())
                    if abs(c_val.imag) > 1e-9:
                        all_positive_real = False
                        break
                    if c_val.real <= 0:
                        all_positive_real = False
                        break
            except Exception:
                try:
                    if not bool(val > 0):
                        all_positive_real = False
                        break
                except Exception:
                    all_positive_real = False
                    break
        neg_q = not all_positive_real
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "H_2: A is Hermitian",
    "¬Q: Not all eigenvalues of A are strictly positive real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2