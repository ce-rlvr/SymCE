import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n matrix over the complex numbers
    try:
        h1 = hasattr(witness, 'is_square') and witness.is_square
    except Exception:
        h1 = False

    # neg_Q: A is not unitarily diagonalizable
    # A complex square matrix is unitarily diagonalizable iff it is normal (A * A^H == A^H * A)
    try:
        if not h1:
            neg_q = False
        else:
            A = witness
            A_H = A.H
            diff = A * A_H - A_H * A
            
            # Check if the difference is the zero matrix
            if diff == zeros(A.rows, A.cols):
                is_normal = True
            else:
                # Fallback to symbolic simplification if exact equality fails
                diff_simp = sympy.simplify(diff)
                is_normal = (diff_simp == zeros(A.rows, A.cols))
                
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over the complex numbers",
    "¬Q: A is not unitarily diagonalizable (i.e., A is not normal)"
]

N_HYP = 1
NEG_Q_INDEX = 1