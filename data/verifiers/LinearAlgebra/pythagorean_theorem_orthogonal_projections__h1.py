import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        P, x = witness
        if not isinstance(P, Matrix):
            P = Matrix(P)
        if not isinstance(x, Matrix):
            x = Matrix(x)
        if x.shape[0] == 1:
            x = x.T
        h1 = P.is_square and P.shape[1] == x.shape[0] and x.shape[1] == 1
    except Exception:
        h1 = False

    try:
        P, x = witness
        if not isinstance(P, Matrix):
            P = Matrix(P)
        if not isinstance(x, Matrix):
            x = Matrix(x)
        if x.shape[0] == 1:
            x = x.T
            
        norm_x_sq = (x.H * x)[0, 0]
        Px = P * x
        norm_Px_sq = (Px.H * Px)[0, 0]
        x_minus_Px = x - Px
        norm_x_minus_Px_sq = (x_minus_Px.H * x_minus_Px)[0, 0]
        
        diff = sympy.expand(norm_x_sq - (norm_Px_sq + norm_x_minus_Px_sq))
        try:
            neg_q = abs(complex(diff)) > 1e-9
        except TypeError:
            neg_q = bool(sympy.simplify(diff) != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an arbitrary vector in V",
    "¬Q: The squared norm of x is NOT equal to the sum of the squared norm of Px and the squared norm of x - Px"
]

N_HYP = 1
NEG_Q_INDEX = 1