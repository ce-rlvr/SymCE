import sympy
import math

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (A, m, n)
    where A is a sympy.Matrix, and m, n are integers.
    """
    try:
        A, m, n = witness
    except Exception:
        return [False, False]
        
    # H_1: A is a square matrix with integer entries
    try:
        h1 = isinstance(A, sympy.Matrix) and A.is_square
        if h1:
            h1 = all(isinstance(x, (int, sympy.Integer)) for x in A)
        # The moduli m and n must also be integers
        h1 = bool(h1 and isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)))
    except Exception:
        h1 = False
        
    # ¬Q: The matrix A is invertible modulo mn is NOT equivalent to 
    #     (A is invertible modulo m and A is invertible modulo n)
    try:
        detA = int(A.det())
        m_int = int(m)
        n_int = int(n)
        
        # A square matrix with integer entries is invertible modulo k 
        # if and only if its determinant is coprime to k.
        inv_mn = math.gcd(detA, m_int * n_int) == 1
        inv_m = math.gcd(detA, m_int) == 1
        inv_n = math.gcd(detA, n_int) == 1
        
        # The conclusion states: inv_mn == (inv_m and inv_n)
        # The negated conclusion is that this equivalence fails.
        neg_q = bool(inv_mn != (inv_m and inv_n))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix with integer entries",
    "¬Q: The matrix A is invertible modulo mn is NOT equivalent to (A is invertible modulo m and A is invertible modulo n)"
]

N_HYP = 1
NEG_Q_INDEX = 1