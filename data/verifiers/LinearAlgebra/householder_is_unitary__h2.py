import sympy
from sympy import Matrix, eye, simplify, expand

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Extract v from witness
        if isinstance(witness, dict) and 'v' in witness:
            v = witness['v']
        elif isinstance(witness, tuple):
            v = witness[0]
        else:
            v = witness
            
        # Ensure v is a SymPy Matrix
        if not isinstance(v, Matrix):
            v = Matrix(v)
            
        # H_1: v is a non-zero column vector in C^n
        h1 = False
        if len(v.shape) == 2 and v.shape[1] == 1 and v.is_zero_matrix != True:
            h1 = True
            
        # neg_Q: H is not a unitary matrix
        neg_q = False
        if h1:
            n = v.shape[0]
            # Standard Householder transformation definition: H = I - 2 * v * v^H
            H = eye(n) - 2 * v * v.H
            
            # Check if H is unitary (H^H * H == I)
            prod = expand(H.H * H)
            if prod != eye(n):
                if simplify(prod) != eye(n):
                    neg_q = True
                    
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: v is a non-zero column vector in C^n",
    "¬Q: H is not a unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1