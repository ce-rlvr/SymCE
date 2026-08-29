import sympy
from sympy import Matrix, eye, zeros, simplify
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            h1 = all(e.is_real for e in witness)
    except Exception:
        h1 = False

    try:
        n = witness.rows
        E = witness.exp()
        diff = E.T * E - eye(n)
        diff = simplify(diff)
        is_orthogonal = diff.is_zero_matrix
        if is_orthogonal is None:
            is_orthogonal = diff == zeros(n, n)
        neg_q = not is_orthogonal
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a real n x n matrix",
    "¬Q: The matrix exponential e^A is not an orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1