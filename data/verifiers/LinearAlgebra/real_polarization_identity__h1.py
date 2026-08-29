import sympy
from sympy import Matrix, simplify, expand, eye, zeros

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        u, v = witness
    except Exception:
        return [False, False]
    
    # H_1: u and v are vectors in V
    try:
        h1 = (hasattr(u, 'shape') and hasattr(v, 'shape') and 
              len(u.shape) == 2 and len(v.shape) == 2 and
              u.shape == v.shape and u.shape[1] == 1 and
              hasattr(u, 'adjoint') and hasattr(v, 'adjoint'))
    except Exception:
        h1 = False

    # ¬Q: <u, v> != 1/4(||u + v||^2 - ||u - v||^2)
    try:
        def inner(x, y):
            # Standard complex inner product
            return (x.adjoint() * y)[0, 0]
        
        def norm_sq(x):
            return inner(x, x)
        
        lhs = inner(u, v)
        rhs = (norm_sq(u + v) - norm_sq(u - v)) / 4
        
        diff = simplify(expand(lhs - rhs))
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: u and v are vectors in V",
    "¬Q: <u, v> != 1/4(||u + v||^2 - ||u - v||^2)"
]

N_HYP = 1
NEG_Q_INDEX = 1