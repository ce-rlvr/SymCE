import sympy
from sympy import I, eye, zeros, Matrix

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (U, x) where U is a unitary matrix and x is a vector.
    """
    try:
        if len(witness) != 2:
            return [False, False, False]
        U, x = witness
    except Exception:
        return [False, False, False]
        
    # H1: U is a unitary matrix
    try:
        if hasattr(U, 'is_unitary') and U.is_unitary:
            h1 = True
        elif hasattr(U, 'is_square') and U.is_square:
            # Fallback check for unitary matrix: U^H * U == I
            diff = U.H * U - sympy.eye(U.rows)
            h1 = all(sympy.simplify(e) == 0 for e in diff)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: x is an arbitrary vector in C^n
    try:
        if isinstance(x, (list, tuple)):
            x_mat = sympy.Matrix(x)
        else:
            x_mat = x
            
        # Check if x is a column vector
        if hasattr(x_mat, 'cols') and x_mat.cols == 1 and hasattr(x_mat, 'rows') and x_mat.rows >= 1:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The Euclidean norm of Ux is NOT equal to the Euclidean norm of x
    try:
        Ux = U * x_mat
        norm_Ux = Ux.norm()
        norm_x = x_mat.norm()
        diff = sympy.simplify(norm_Ux - norm_x)
        neg_q = (diff != 0)
    except Exception:
        # If U * x_mat raises an exception (e.g., dimension mismatch), 
        # the conclusion "||Ux|| == ||x||" cannot hold, so it fails.
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "H_2: x is an arbitrary vector in C^n",
    "¬Q: The Euclidean norm of Ux is not equal to the Euclidean norm of x (or Ux is undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2