import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            M = witness.get('M')
            if M is None and A is not None and B is not None:
                try:
                    M = A.row_join(B).col_join(B.row_join(A))
                except Exception:
                    pass
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                A, B = witness
                M = A.row_join(B).col_join(B.row_join(A))
            elif len(witness) == 3:
                A, B, M = witness
            else:
                A, B, M = None, None, None
        else:
            A, B, M = None, None, None
    except Exception:
        A, B, M = None, None, None

    try:
        h1 = isinstance(A, Matrix) and isinstance(B, Matrix) and A.is_square and B.is_square and A.shape == B.shape
    except Exception:
        h1 = False

    try:
        h2 = bool((A + B).is_diagonalizable())
    except Exception:
        h2 = False

    try:
        M_expected = A.row_join(B).col_join(B.row_join(A))
        h3 = bool(M == M_expected)
    except Exception:
        h3 = False

    try:
        neg_q = not bool(M.is_diagonalizable())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n matrices over a field F with char != 2",
    "H_2: A+B is diagonalizable over F",
    "H_3: M is the 2n x 2n block matrix having A on main diagonal and B on off-diagonal",
    "¬Q: M is not diagonalizable over F"
]

N_HYP = 3
NEG_Q_INDEX = 3