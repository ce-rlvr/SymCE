import sympy
from sympy.matrices import MatrixBase, zeros, eye

O0 = zeros(0, 0)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # We interpret a SymPy matrix as a linear transformation over C 
        # (which is an algebraically closed field).
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    try:
        # A square matrix represents a linear transformation from V to V.
        h2 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    try:
        if not h2:
            neg_q = False
        elif witness.shape[0] == 0:
            # A 0x0 matrix represents a transformation on a 0-dimensional space,
            # which vacuously has no eigenvectors (as eigenvectors must be non-zero).
            neg_q = True
        else:
            # For dim > 0, check if there are no eigenvectors.
            neg_q = len(witness.eigenvects()) == 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: T: V \\to V is a linear transformation",
    "¬Q: T has no eigenvectors in V"
]

N_HYP = 2
NEG_Q_INDEX = 2