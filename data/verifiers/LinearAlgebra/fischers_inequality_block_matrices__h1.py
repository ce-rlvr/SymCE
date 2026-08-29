import sympy
from sympy import Matrix, BlockMatrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                M, A, B, C = witness
                M = Matrix(M)
                A = Matrix(A)
                B = Matrix(B)
                C = Matrix(C)
            elif len(witness) == 3:
                A, B, C = witness
                A = Matrix(A)
                B = Matrix(B)
                C = Matrix(C)
                M = Matrix(BlockMatrix([[A, B], [B.transpose(), C]]))
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        expected_M = Matrix(BlockMatrix([[A, B], [B.transpose(), C]]))
        h1 = bool(M == expected_M)
    except Exception:
        h1 = False

    try:
        h2 = bool(A.is_square and C.is_square)
    except Exception:
        h2 = False

    try:
        det_M = M.det()
        det_A = A.det()
        det_C = C.det()
        neg_q = bool(det_M > det_A * det_C)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is partitioned into blocks A, B, B^T, C",
    "H_2: The blocks A and C are square matrices",
    "¬Q: det(M) > det(A)det(C)"
]

N_HYP = 2
NEG_Q_INDEX = 2