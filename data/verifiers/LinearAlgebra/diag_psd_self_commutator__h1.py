import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    A = witness
    
    # H_1: The self-commutator A^* A - A A^* is a positive semidefinite matrix
    try:
        if hasattr(A, 'adjoint'):
            if callable(A.adjoint):
                A_star = A.adjoint()
            else:
                A_star = A.adjoint
        elif hasattr(A, 'H'):
            A_star = A.H
        elif hasattr(A, 'T'):
            A_star = A.T
        else:
            return [False, False]
            
        comm = A_star * A - A * A_star
        
        if hasattr(comm, 'is_positive_semidefinite'):
            if callable(comm.is_positive_semidefinite):
                h1 = comm.is_positive_semidefinite()
            else:
                h1 = comm.is_positive_semidefinite
            
            if h1 is None:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: A is not a normal matrix or not unitarily diagonalizable
    try:
        if hasattr(A, 'is_normal'):
            if callable(A.is_normal):
                is_normal = A.is_normal()
            else:
                is_normal = A.is_normal
        else:
            is_normal = bool(A_star * A == A * A_star)
            
        if hasattr(A, 'is_unitarily_diagonalizable'):
            if callable(A.is_unitarily_diagonalizable):
                is_diag = A.is_unitarily_diagonalizable()
            else:
                is_diag = A.is_unitarily_diagonalizable
        elif hasattr(A, 'is_diagonalizable'):
            if callable(A.is_diagonalizable):
                is_diag = A.is_diagonalizable()
            else:
                is_diag = A.is_diagonalizable
        else:
            is_diag = False
            
        q = is_normal and is_diag
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The self-commutator A^* A - A A^* is a positive semidefinite matrix",
    "¬Q: A is not a normal matrix or is not unitarily diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1