import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an m \times n matrix over a field F
    try:
        if isinstance(witness, dict):
            A = witness['A']
            B = witness['B']
        else:
            A, B = witness
        h1_ok = isinstance(A, MatrixBase)
    except Exception:
        h1_ok = False

    # ¬Q: The rank of the Kronecker product A \otimes B is NOT equal to rank(A) \times rank(B)
    try:
        if isinstance(witness, dict):
            A = witness['A']
            B = witness['B']
        else:
            A, B = witness
        
        m, n = A.shape
        p, q = B.shape
        
        # Compute Kronecker product manually to ensure compatibility
        K = Matrix(m * p, n * q, lambda i, j: A[i // p, j // q] * B[i % p, j % q])
        
        rank_K = K.rank()
        rank_A = A.rank()
        rank_B = B.rank()
        
        neg_q_ok = bool(rank_K != rank_A * rank_B)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over a field F",
    "¬Q: rank(A ⊗ B) != rank(A) * rank(B)"
]

N_HYP = 1
NEG_Q_INDEX = 1