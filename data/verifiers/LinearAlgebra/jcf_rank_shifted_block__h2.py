import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    if isinstance(witness, (int, sympy.Integer)):
        k = int(witness)
        lmbda = 0
        M = Matrix.zeros(k, k)
        for i in range(k):
            M[i, i] = lmbda
            if i + 1 < k:
                M[i, i+1] = 1
        return M, lmbda
    elif isinstance(witness, tuple) and len(witness) == 2:
        first, second = witness
        if isinstance(first, (int, sympy.Integer)):
            k = int(first)
            lmbda = second
            M = Matrix.zeros(k, k)
            for i in range(k):
                M[i, i] = lmbda
                if i + 1 < k:
                    M[i, i+1] = 1
            return M, lmbda
        else:
            M = first
            lmbda = second
            if not isinstance(M, Matrix):
                M = Matrix(M)
            return M, lmbda
    else:
        if not isinstance(witness, Matrix):
            M = Matrix(witness)
        else:
            M = witness
        if M.shape[0] > 0:
            lmbda = M[0, 0]
        else:
            lmbda = 0
        return M, lmbda

def is_jordan_block(M, lmbda):
    if not hasattr(M, 'is_square') or not M.is_square:
        return False
    k = M.shape[0]
    for i in range(k):
        for j in range(k):
            if i == j:
                if M[i, j] != lmbda: return False
            elif j == i + 1:
                if M[i, j] != 1: return False
            else:
                if M[i, j] != 0: return False
    return True

def conditions(witness) -> list[bool]:
    try:
        M, lmbda = parse_witness(witness)
    except Exception:
        return [False, False]
    
    try:
        h1 = is_jordan_block(M, lmbda)
    except Exception:
        h1 = False
        
    try:
        k = M.shape[0]
        shifted = M - lmbda * eye(k)
        rank = shifted.rank()
        neg_q = (rank != k - 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: J_k(lambda) is a k x k Jordan block with eigenvalue lambda",
    "¬Q: The rank of J_k(lambda) - lambda*I is not exactly k - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1