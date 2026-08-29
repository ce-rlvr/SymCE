import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a sympy Matrix representing the linear transformation T,
    or a tuple (A, p) where A is the matrix and p is the norm type (defaulting to 2).
    """
    try:
        p = 2
        if isinstance(witness, tuple):
            A = witness[0]
            if len(witness) > 1:
                p = witness[1]
        else:
            A = witness
            
        # H_1 and H_2: A must be a valid matrix representing a linear transformation
        # between finite-dimensional inner product spaces.
        if not hasattr(A, 'norm') or not hasattr(A, 'H'):
            return [False, False, False]
            
        h1 = True
        h2 = True
        
        # Check for the trivial/empty space edge case where supremum definitions of norm
        # can lead to ||T|| = -inf and ||T*|| = 0, breaking the equality.
        if hasattr(A, 'rows') and hasattr(A, 'cols'):
            if (A.rows == 0 and A.cols > 0) or (A.cols == 0 and A.rows > 0):
                return [True, True, True]
                
        try:
            n1 = A.norm(p)
        except Exception:
            n1 = None
            
        try:
            n2 = A.H.norm(p)
        except Exception:
            n2 = None
            
        if n1 is None or n2 is None:
            neg_q = (n1 != n2)
        else:
            diff = sp.simplify(n1 - n2)
            if diff.is_number:
                neg_q = abs(complex(diff)) > 1e-9
            else:
                neg_q = (diff != 0)
                
        return [h1, h2, bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V and W are finite-dimensional inner product spaces over the same field (real or complex)",
    "H_2: T is a linear transformation from V to W",
    "¬Q: The operator norm of T* is not equal to the operator norm of T (||T*|| != ||T||)"
]

N_HYP = 2
NEG_Q_INDEX = 2