import sympy
from sympy import Matrix, eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n \times n matrix with complex entries
    try:
        if not isinstance(witness, sympy.MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            h1 = True
            for entry in witness:
                # is_complex is False for things like infinity
                if entry.is_complex is False:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # neg_Q: The complex conjugate matrix \overline{A} is NOT diagonalizable over C
    try:
        if h1:
            A_conj = witness.conjugate()
            is_diag = A_conj.is_diagonalizable()
            # We specifically want is_diag to be False (not True and not None)
            neg_q = (is_diag is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with complex entries",
    "¬Q: The complex conjugate matrix is not diagonalizable over the complex numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1