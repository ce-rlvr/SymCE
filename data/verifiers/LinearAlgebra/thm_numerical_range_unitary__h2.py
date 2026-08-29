import sympy
from sympy import Matrix, eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            U = witness['U']
            x = witness['x']
        else:
            U, x = witness
        
        U = Matrix(U)
        x = Matrix(x)
        
        n = U.shape[0]
        h1 = False
        if U.shape == (n, n) and x.shape == (n, 1):
            diff = U.H * U - eye(n)
            is_zero = diff.is_zero_matrix
            if is_zero is True:
                h1 = True
            else:
                try:
                    max_val = max(float(sympy.Abs(diff[i, j].evalf())) for i in range(n) for j in range(n))
                    if max_val < 1e-9:
                        h1 = True
                    else:
                        h1 = all(sympy.simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
                except Exception:
                    h1 = all(sympy.simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            U = witness['U']
            x = witness['x']
        else:
            U, x = witness
            
        U = Matrix(U)
        x = Matrix(x)
        
        val = (x.H * U * x)[0]
        abs_val = sympy.Abs(val)
        
        if abs_val.is_number:
            neg_q = float(abs_val.evalf()) > 1.0 + 1e-9
        else:
            neg_q = bool(sympy.simplify(abs_val) > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n unitary matrix",
    "¬Q: The absolute value of x^* U x is greater than 1"
]

N_HYP = 1
NEG_Q_INDEX = 1