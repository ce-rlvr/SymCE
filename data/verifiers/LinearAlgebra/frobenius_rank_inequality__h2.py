import sympy as sp
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B, C = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(isinstance(A, MatrixBase) or getattr(A, 'is_Matrix', False))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(isinstance(C, MatrixBase) or getattr(C, 'is_Matrix', False))
    except Exception:
        h2 = False
        
    try:
        def get_rank(X):
            if hasattr(X, 'rank') and callable(X.rank):
                return X.rank()
            if isinstance(X, (int, float, complex)):
                return 1 if X != 0 else 0
            if hasattr(X, 'is_zero'):
                if X.is_zero is True:
                    return 0
                elif X.is_zero is False:
                    return 1
            if isinstance(X, sp.Expr):
                return 1
            raise ValueError(f"Cannot compute rank of {type(X)}")
            
        AB = A * B
        BC = B * C
        ABC = A * B * C
        
        rank_AB = get_rank(AB)
        rank_BC = get_rank(BC)
        rank_B = get_rank(B)
        rank_ABC = get_rank(ABC)
        
        neg_q = bool(rank_AB + rank_BC > rank_B + rank_ABC)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over a field F",
    "H_2: C is a p x q matrix over the field F",
    "¬Q: rank(AB) + rank(BC) > rank(B) + rank(ABC)"
]

N_HYP = 2
NEG_Q_INDEX = 2