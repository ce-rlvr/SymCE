import sympy as sp
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            A, r = witness
        else:
            A = witness
            # If r is not provided, compute it so H1 is satisfied
            if hasattr(A, "singular_values"):
                svals = A.singular_values()
                r = 0
                for s in svals:
                    try:
                        if s.is_number:
                            if s.evalf() > 0:
                                r += 1
                        else:
                            if s > 0:
                                r += 1
                    except Exception:
                        pass
            else:
                return [False, False]
    except Exception:
        return [False, False]

    # H1: A has exactly r strictly positive singular values, counted with algebraic multiplicity
    try:
        svals = A.singular_values()
        pos_count = 0
        for s in svals:
            try:
                if s.is_number:
                    if s.evalf() > 0:
                        pos_count += 1
                else:
                    if s > 0:
                        pos_count += 1
            except Exception:
                pass
        h1 = (pos_count == r)
    except Exception:
        h1 = False

    # neg_Q: The rank of the matrix A is not equal to r
    try:
        neg_q = bool(A.rank() != r)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A has exactly r strictly positive singular values, counted with algebraic multiplicity",
    "¬Q: The rank of the matrix A is not equal to r"
]

N_HYP = 1
NEG_Q_INDEX = 1