import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple of two elements (a, b)
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        a, b = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = False
        # Check if a and b are square matrices of the same size (matrix rings over fields are Artinian)
        if hasattr(a, 'is_Matrix') and a.is_Matrix and hasattr(b, 'is_Matrix') and b.is_Matrix:
            if a.shape == b.shape and a.shape[0] == a.shape[1]:
                h1 = True
        else:
            # Alternatively, check if they are scalars (fields are Artinian rings)
            def is_scalar(x):
                if isinstance(x, (int, float)):
                    return True
                if hasattr(x, 'is_number') and x.is_number:
                    return True
                return False
            if is_scalar(a) and is_scalar(b):
                h1 = True
    except Exception:
        h1 = False
        
    try:
        neg_q = False
        if h1:
            if hasattr(a, 'is_Matrix') and a.is_Matrix:
                n = a.shape[0]
                I = eye(n)
                neg_q = bool(b * a != I)
            else:
                neg_q = bool(b * a != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Elements a and b belong to a right Artinian ring (e.g., a field or square matrices over a field)",
    "¬Q: ba != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1