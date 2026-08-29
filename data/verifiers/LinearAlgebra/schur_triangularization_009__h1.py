import sympy
from sympy import Matrix, eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: The entries of A are complex numbers
    try:
        if not isinstance(witness, sympy.MatrixBase):
            A = Matrix(witness)
        else:
            A = witness
        
        # Check that all entries are explicitly complex numbers (no free symbols)
        h1 = all(sympy.sympify(x).is_complex is True for x in A)
    except Exception:
        h1 = False

    # ¬Q: There do not exist a unitary matrix U and an upper triangular matrix T such that A = U T U^*
    # By Schur's Triangularization Theorem, such U and T exist for ALL square complex matrices.
    # Therefore, the conclusion fails if and only if A is not a square matrix.
    try:
        if not isinstance(witness, sympy.MatrixBase):
            A = Matrix(witness)
        else:
            A = witness
            
        neg_q = not A.is_square
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The entries of A are complex numbers",
    "¬Q: There do not exist a unitary matrix U and an upper triangular matrix T such that A = U T U^*"
]

N_HYP = 1
NEG_Q_INDEX = 1