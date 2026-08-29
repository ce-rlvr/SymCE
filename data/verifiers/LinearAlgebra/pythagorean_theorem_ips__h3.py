import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        u, v = witness
        
        if not isinstance(u, Matrix):
            u = Matrix(u)
        if not isinstance(v, Matrix):
            v = Matrix(v)
            
        # Ensure they are column vectors
        if u.shape[0] == 1:
            u = u.T
        if v.shape[0] == 1:
            v = v.T
            
        h1 = (isinstance(u, Matrix) and isinstance(v, Matrix) and 
              u.shape == v.shape and u.shape[1] == 1)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Compute ||u + v||^2
            norm_sum_sq = ((u + v).H * (u + v))[0]
            # Compute ||u||^2 + ||v||^2
            sum_norm_sq = (u.H * u)[0] + (v.H * v)[0]
            
            # Check if they are strictly unequal
            diff = sympy.simplify(norm_sum_sq - sum_norm_sq)
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: u and v are vectors in an inner product space",
    "¬Q: ||u + v||^2 != ||u||^2 + ||v||^2"
]

N_HYP = 1
NEG_Q_INDEX = 1