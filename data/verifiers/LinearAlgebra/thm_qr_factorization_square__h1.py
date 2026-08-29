import sympy
from sympy import Matrix, I, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "There exists an n x n real orthogonal matrix Q and an n x n upper triangular matrix R such that A = Q R."
    
    Since any real square matrix has a real QR factorization, a counterexample 
    must be a square matrix that is NOT real (e.g., a complex matrix).
    """
    try:
        # Allow lists of lists to be automatically converted to a Matrix
        if isinstance(witness, list):
            A = Matrix(witness)
        else:
            A = witness
            
        # Witness must be a square matrix
        if not isinstance(A, sympy.MatrixBase):
            return [False]
        if not A.is_square:
            return [False]
            
        # Check if the matrix has only real entries
        is_real = True
        for val in A:
            # If an entry is explicitly non-real or contains the imaginary unit
            if val.is_real is False or val.has(sympy.I):
                is_real = False
                break
                
        # The conclusion FAILS (neg_Q is True) if the matrix is not real,
        # because a non-real matrix cannot be the product of a real Q and a real R.
        neg_q = not is_real
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A does not have a real QR factorization (e.g., A is a complex square matrix)"
]

N_HYP = 0
NEG_Q_INDEX = 0