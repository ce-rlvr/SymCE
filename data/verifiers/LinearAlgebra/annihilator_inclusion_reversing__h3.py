import sympy
from sympy.matrices import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) >= 2:
            W1, W2 = witness[-2], witness[-1]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(W1, Matrix) and isinstance(W2, Matrix)
    except Exception:
        h1 = False
        
    try:
        h2 = h1 and (W1.cols == W2.cols)
    except Exception:
        h2 = False
        
    try:
        if not h2:
            neg_q = False
        else:
            null2 = W2.nullspace()
            neg_q = False
            for v in null2:
                prod = W1 * v
                if not all(val == 0 for val in prod):
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: W_1 and W_2 are subspaces of V",
    "¬Q: W_2^0 is not a subspace of W_1^0"
]

N_HYP = 2
NEG_Q_INDEX = 2