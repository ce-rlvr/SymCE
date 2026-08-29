import sympy
from sympy import eye, zeros, sqrt

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, list):
            U = sympy.Matrix(witness)
        else:
            U = witness
            
        if not hasattr(U, 'rows'):
            return [False]
            
        n = U.rows
        norm = U.norm()
        diff = sympy.simplify(norm - sqrt(n))
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Frobenius norm of U is not exactly equal to the square root of n"
]

N_HYP = 0
NEG_Q_INDEX = 0