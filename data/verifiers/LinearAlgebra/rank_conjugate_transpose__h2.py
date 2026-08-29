import sympy
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let A be an m x n matrix over the field of complex numbers C
    try:
        h1 = isinstance(witness, sympy.matrices.MatrixBase)
    except Exception:
        h1 = False

    # ¬Q: The rank of A^* is NOT equal to the rank of A
    try:
        # A^* denotes the conjugate transpose (Hermitian adjoint), which is .H in SymPy
        neg_q = witness.H.rank() != witness.rank()
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over the field of complex numbers C",
    "¬Q: The rank of A^* is not equal to the rank of A"
]

N_HYP = 1
NEG_Q_INDEX = 1