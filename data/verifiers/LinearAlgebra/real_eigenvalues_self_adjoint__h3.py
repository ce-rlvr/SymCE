import sympy
from sympy import Matrix, eye, zeros, I, im, re, N

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: V is an inner product space
    # In finite dimensions, we represent the space and operator via a matrix.
    try:
        h1 = isinstance(witness, sympy.MatrixBase)
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V
    # This corresponds to the matrix being square.
    try:
        h2 = h1 and witness.is_square
    except Exception:
        h2 = False

    # ¬Q: Every eigenvalue of T is a real number (Negation: T has at least one non-real eigenvalue)
    try:
        neg_q = False
        if h2:
            evs = witness.eigenvals()
            for val in evs.keys():
                val_n = N(val)
                imag_part = im(val_n)
                if abs(float(imag_part)) > 1e-12:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space (witness is a matrix)",
    "H_2: T is a linear operator on V (witness is a square matrix)",
    "¬Q: T has at least one non-real eigenvalue"
]

N_HYP = 2
NEG_Q_INDEX = 2