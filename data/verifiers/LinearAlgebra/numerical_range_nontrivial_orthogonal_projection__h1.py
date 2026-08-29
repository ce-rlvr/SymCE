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

def conditions(witness):
    # H_1: P is neither the zero matrix nor the identity matrix
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square:
            h1 = False
        else:
            n = witness.rows
            h1 = bool(witness != zeros(n, n) and witness != eye(n))
    except Exception:
        h1 = False

    # neg_Q: The numerical range of P is NOT the real closed interval [0, 1]
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square:
            neg_q = False
        elif witness != witness.H:
            # If P is not Hermitian, its numerical range cannot be a subset of the real line
            neg_q = True
        else:
            # For a Hermitian matrix, the numerical range is the real interval [min_eig, max_eig]
            eigs = witness.eigenvals()
            eig_vals = [complex(e.evalf()).real for e in eigs.keys()]
            min_e = min(eig_vals)
            max_e = max(eig_vals)
            if abs(min_e) < 1e-7 and abs(max_e - 1.0) < 1e-7:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is neither the zero matrix nor the identity matrix",
    "¬Q: The numerical range of P is not the real closed interval from 0 to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1