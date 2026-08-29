import sympy
from sympy.matrices import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        x, y = witness
    except Exception:
        return [False, False]
    
    try:
        _ = x + y
        _ = x * y
        h1 = True
    except Exception:
        h1 = False
        
    try:
        neg_q = not bool(x * y == y * x)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of R",
    "¬Q: x * y != y * x"
]

N_HYP = 1
NEG_Q_INDEX = 1