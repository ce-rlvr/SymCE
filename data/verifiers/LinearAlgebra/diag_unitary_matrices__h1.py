import sympy
from sympy import eye, zeros, Matrix, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A satisfies A^* A = I
    try:
        if not isinstance(witness, sympy.MatrixBase):
            h1 = False
        else:
            cols = witness.shape[1]
            diff = witness.H * witness - eye(cols)
            if diff.is_zero_matrix:
                h1 = True
            else:
                diff_simp = sympy.simplify(diff)
                h1 = bool(diff_simp.is_zero_matrix)
    except Exception:
        h1 = False

    # ¬Q: A is not diagonalizable over the complex numbers
    try:
        if not isinstance(witness, sympy.MatrixBase):
            neg_q = False
        elif not witness.is_square:
            # Non-square matrices cannot be diagonalized
            neg_q = True
        else:
            is_diag = witness.is_diagonalizable()
            if is_diag is None:
                neg_q = False
            else:
                neg_q = not bool(is_diag)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A satisfies A^* A = I",
    "¬Q: A is not diagonalizable over the complex numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1