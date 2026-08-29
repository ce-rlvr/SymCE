import sympy
from sympy import Matrix, eye, zeros, I, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        U, x, y = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = hasattr(U, 'is_square') and U.is_square and hasattr(U, 'shape')
    except Exception:
        h1 = False
        
    try:
        if h1:
            n = U.shape[0]
            x_mat = Matrix(x) if not hasattr(x, 'shape') else x
            y_mat = Matrix(y) if not hasattr(y, 'shape') else y
            
            if x_mat.shape == (1, n):
                x_mat = x_mat.T
            if y_mat.shape == (1, n):
                y_mat = y_mat.T
                
            h2 = hasattr(x_mat, 'shape') and hasattr(y_mat, 'shape') and x_mat.shape == (n, 1) and y_mat.shape == (n, 1)
            x = x_mat
            y = y_mat
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        if h1 and h2:
            Ux = U * x
            Uy = U * y
            ip_Ux_Uy = Ux.adjoint() * Uy
            ip_x_y = x.adjoint() * y
            
            eq = ip_Ux_Uy.equals(ip_x_y)
            if eq is None:
                diff = simplify((ip_Ux_Uy - ip_x_y)[0, 0])
                neg_q = diff != 0
            else:
                neg_q = not eq
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "H_2: x and y are vectors in C^n",
    "¬Q: The standard inner product of Ux and Uy is not equal to the standard inner product of x and y"
]

N_HYP = 2
NEG_Q_INDEX = 2