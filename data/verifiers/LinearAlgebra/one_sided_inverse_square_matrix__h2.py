import sympy
from sympy.matrices import MatrixBase, Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
        if not isinstance(A, MatrixBase):
            A = Matrix(A)
        if not isinstance(B, MatrixBase):
            B = Matrix(B)
        h1 = bool(A.is_square and B.is_square and A.shape == B.shape)
    except Exception:
        h1 = False

    try:
        A, B = witness
        if not isinstance(A, MatrixBase):
            A = Matrix(A)
        if not isinstance(B, MatrixBase):
            B = Matrix(B)
            
        if not (A.is_square and B.is_square and A.shape == B.shape):
            neg_q = False
        else:
            n = A.shape[0]
            prod = B * A
            I = eye(n)
            eq = prod.equals(I)
            if eq is None:
                neg_q = bool(prod != I)
            else:
                neg_q = not eq
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n matrices",
    "¬Q: BA != I_n"
]

N_HYP = 1
NEG_Q_INDEX = 1