import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A_raw, B_raw = witness
        A = Matrix(A_raw)
        B = Matrix(B_raw)
    except Exception:
        return [False, False]
    
    # H_1: A is an n x n real orthogonal matrix
    try:
        if A.rows != A.cols or A.rows < 1:
            h1 = False
        else:
            is_real = all((hasattr(e, 'is_real') and e.is_real is True) for e in A)
            if is_real:
                # Check if A^T * A == I
                h1 = bool(sympy.expand(A.T * A) == eye(A.rows))
            else:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: A ⊗ B is NOT an nm x nm real orthogonal matrix
    try:
        n = A.rows
        m = B.rows
        if B.cols != m:
            # B is not square, so A ⊗ B cannot be an nm x nm matrix
            neg_q = True
        elif m < 1:
            neg_q = True
        else:
            # Compute the Kronecker product A ⊗ B
            K = Matrix(n * m, n * m, lambda i, j: A[i // m, j // m] * B[i % m, j % m])
            
            is_K_real = all((hasattr(e, 'is_real') and e.is_real is True) for e in K)
            if not is_K_real:
                neg_q = True
            else:
                # Check if K^T * K == I
                is_K_ortho = bool(sympy.expand(K.T * K) == eye(n * m))
                neg_q = not is_K_ortho
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real orthogonal matrix",
    "¬Q: A ⊗ B is not an nm x nm real orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1