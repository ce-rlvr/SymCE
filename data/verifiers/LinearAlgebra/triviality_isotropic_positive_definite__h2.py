import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        B = Matrix(witness[0])
        v = Matrix(witness[1])
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (B.is_square and 
              v.shape[1] == 1 and 
              B.shape[0] == v.shape[0] and 
              all(x.is_real for x in B) and 
              all(x.is_real for x in v))
    except Exception:
        h1 = False

    try:
        val = (v.T * B * v)[0, 0]
        h2 = (sympy.simplify(val) == 0)
    except Exception:
        h2 = False

    try:
        neg_q = not v.is_zero_matrix
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over the real numbers",
    "H_2: v is an isotropic vector with respect to B, meaning B(v, v) = 0",
    "¬Q: v is not the zero vector"
]

N_HYP = 2
NEG_Q_INDEX = 2