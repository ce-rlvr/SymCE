import sympy
from sympy import eye, zeros, simplify
from sympy.matrices import MatrixBase

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_unitary(M):
    try:
        if not isinstance(M, MatrixBase):
            return False
        if not getattr(M, 'is_square', False):
            return False
        n = M.shape[0]
        prod = M * M.H
        Id = eye(n)
        if prod == Id:
            return True
        diff = prod - Id
        for i in range(n):
            for j in range(n):
                if simplify(diff[i, j]) != 0:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        U, V = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: V is an n x n complex matrix
    try:
        h1_ok = isinstance(V, MatrixBase) and getattr(V, 'is_square', False)
    except Exception:
        h1_ok = False
        
    # H_2: U is a unitary matrix
    try:
        h2_ok = is_unitary(U)
    except Exception:
        h2_ok = False
        
    # H_3: V is a unitary matrix
    try:
        h3_ok = is_unitary(V)
    except Exception:
        h3_ok = False
        
    # ¬Q: The matrix product UV is not a unitary matrix
    try:
        UV = U * V
        neg_q_ok = not is_unitary(UV)
    except Exception:
        # If the product is undefined (e.g., due to dimension mismatch), 
        # then UV is not a unitary matrix.
        neg_q_ok = True
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is an n x n complex matrix",
    "H_2: U is a unitary matrix",
    "H_3: V is a unitary matrix",
    "¬Q: The matrix product UV is not a unitary matrix"
]

N_HYP = 3
NEG_Q_INDEX = 3