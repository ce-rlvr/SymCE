import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
O2 = zeros(2, 2)
I3 = eye(3)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                B, C = witness
            elif len(witness) == 3:
                _, B, C = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        try:
            if not isinstance(B, Matrix):
                B = Matrix(B)
            if not isinstance(C, Matrix):
                C = Matrix(C)
        except Exception:
            return [False, False, False]
            
        h1 = bool(B.is_square)
        h2 = bool(C.is_square and C.shape == B.shape)
        
        if not (h1 and h2):
            return [False, False, False]
            
        neg_q = bool(B.det() == 0)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: C is a bilinear form on V",
    "¬Q: There does not exist a unique linear operator T such that C(x, y) = B(T(x), y)"
]

N_HYP = 2
NEG_Q_INDEX = 2