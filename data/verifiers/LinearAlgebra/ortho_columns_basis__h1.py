import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not getattr(witness, "is_Matrix", False):
            Q = sympy.Matrix(witness)
        else:
            Q = witness
    except Exception:
        return [False, False]

    try:
        cols = Q.shape[1]
        diff = Q.T * Q - sympy.eye(cols)
        if diff.is_zero_matrix:
            h1 = True
        else:
            h1 = bool(sympy.simplify(diff).is_zero_matrix)
    except Exception:
        h1 = False

    try:
        if not Q.is_square:
            is_orthogonal = False
        else:
            diff2 = Q.T * Q - sympy.eye(Q.shape[0])
            if diff2.is_zero_matrix:
                is_orthogonal = True
            else:
                is_orthogonal = bool(sympy.simplify(diff2).is_zero_matrix)
        neg_q = not is_orthogonal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The columns of Q form an orthonormal set under the standard Euclidean inner product",
    "¬Q: Q is not an orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1