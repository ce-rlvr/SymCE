import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Extract the matrix A from the witness
        if isinstance(witness, tuple) and len(witness) > 0 and isinstance(witness[0], sp.MatrixBase):
            A = witness[0]
        else:
            A = witness
            
        # Ensure A is a sympy Matrix
        if not isinstance(A, sp.MatrixBase):
            A = sp.Matrix(A)
            
        m, n = A.shape
        
        # H_1: A is a real matrix
        try:
            h1 = all(sp.sympify(A[i, j]).is_real != False for i in range(m) for j in range(n))
        except Exception:
            h1 = False
            
        # H_2: A has full column rank n
        try:
            h2 = (A.rank() == n)
        except Exception:
            h2 = False
            
        # ¬Q: The conclusion fails
        # The conclusion states the image is an n-dimensional hyperellipsoid in R^m.
        # A true n-dimensional hyperellipsoid in R^m requires m = n (it must have m principal semi-axes).
        # If m > n, the image is a degenerate hyperellipsoid (flat in m-n dimensions),
        # so it is not an n-dimensional hyperellipsoid in R^m.
        try:
            neg_q = (m != n)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: A is a real matrix",
    "H_2: A has full column rank n",
    "¬Q: The image is not an n-dimensional hyperellipsoid in R^m (m != n)"
]

N_HYP = 2
NEG_Q_INDEX = 2