import sympy
from sympy import eye, simplify, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # If witness is a tuple of dimensions (n, m)
        if isinstance(witness, tuple) and len(witness) == 2:
            n, m = witness
            if isinstance(n, int) and isinstance(m, int):
                # If n != m, the extreme points of the n x m spectral norm ball 
                # are not n x n orthogonal matrices.
                return [bool(n != m)]
        
        # If witness is a matrix (or can be converted to one)
        A = witness
        if isinstance(A, (list, tuple)):
            try:
                A = sympy.Matrix(A)
            except Exception:
                pass
                
        if hasattr(A, 'rows') and hasattr(A, 'cols') and hasattr(A, 'T'):
            I_c = eye(A.cols)
            I_r = eye(A.rows)
            
            extreme = False
            # Check if A is an extreme point of the spectral norm ball
            # (i.e., A has orthonormal columns or orthonormal rows)
            if A.rows >= A.cols:
                diff = A.T * A - I_c
                if all(e == 0 or getattr(e, 'is_zero', False) or simplify(e) == 0 for e in diff):
                    extreme = True
            if A.rows <= A.cols:
                diff = A * A.T - I_r
                if all(e == 0 or getattr(e, 'is_zero', False) or simplify(e) == 0 for e in diff):
                    extreme = True
                    
            square_ortho = False
            # Check if A is a square orthogonal matrix
            if A.rows == A.cols:
                diff = A.T * A - I_c
                if all(e == 0 or getattr(e, 'is_zero', False) or simplify(e) == 0 for e in diff):
                    square_ortho = True
                    
            # The conclusion fails if there is an extreme point that is NOT a square orthogonal matrix
            neg_q = extreme and not square_ortho
            return [bool(neg_q)]
            
        return [False]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The set of extreme points of S is not exactly the set of all real n x n orthogonal matrices"
]

N_HYP = 0
NEG_Q_INDEX = 0