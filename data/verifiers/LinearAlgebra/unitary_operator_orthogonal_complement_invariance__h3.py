import sympy
from sympy import Matrix, eye, zeros, simplify
from sympy.matrices.matrixbase import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            U = witness.get('U')
        else:
            T, U = witness
            
        if isinstance(U, list):
            if len(U) > 0 and all(isinstance(v, MatrixBase) for v in U):
                U = Matrix.hstack(*U)
            elif len(U) == 0 and isinstance(T, MatrixBase):
                U = zeros(T.shape[0], 0)
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(T, MatrixBase) and isinstance(U, MatrixBase) and T.is_square and T.shape[0] == U.shape[0]
    except Exception:
        h1 = False

    try:
        if h1:
            n = T.shape[0]
            diff = T.H * T - eye(n)
            if diff.is_zero_matrix:
                h2 = True
            else:
                h2 = all(simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            null_basis = U.H.nullspace()
            neg_q = False
            for v in null_basis:
                prod = U.H * T * v
                if not prod.is_zero_matrix:
                    is_zero = all(simplify(prod[i, 0]) == 0 for i in range(prod.shape[0]))
                    if not is_zero:
                        neg_q = True
                        break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: T is a unitary operator on V",
    "¬Q: The orthogonal complement U^\\perp is not a T-invariant subspace"
]

N_HYP = 2
NEG_Q_INDEX = 2