import sympy
from sympy import Matrix, MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def kron(A, B):
    return Matrix(A.rows * B.rows, A.cols * B.cols, lambda i, j: A[i // B.rows, j // B.cols] * B[i % B.rows, j % B.cols])

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, B = witness
        else:
            return [False, False]
            
        if isinstance(A, (list, tuple)):
            A = Matrix(A)
        if isinstance(B, (list, tuple)):
            B = Matrix(B)
    except Exception:
        return [False, False]

    # H1: B is a real symmetric m x m positive definite matrix
    try:
        h1 = False
        if isinstance(B, MatrixBase) and B.is_square and B.rows > 0:
            if all(e.is_real == True for e in B) and B.is_symmetric():
                h1 = True
                for i in range(1, B.rows + 1):
                    det = B[:i, :i].det()
                    if det.is_real != True or bool(det <= 0):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: The Kronecker product of A and B is NOT a real symmetric positive definite matrix
    try:
        neg_q = False
        if not isinstance(A, MatrixBase) or not isinstance(B, MatrixBase):
            neg_q = True
        else:
            K = kron(A, B)
            is_K_rspd = True
            if not K.is_square or K.rows == 0:
                is_K_rspd = False
            elif not all(e.is_real == True for e in K):
                is_K_rspd = False
            elif not K.is_symmetric():
                is_K_rspd = False
            else:
                for i in range(1, K.rows + 1):
                    det = K[:i, :i].det()
                    if det.is_real != True or bool(det <= 0):
                        is_K_rspd = False
                        break
            neg_q = not is_K_rspd
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: B is a real symmetric m x m positive definite matrix",
    "¬Q: The Kronecker product of A and B is not a real symmetric positive definite matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1