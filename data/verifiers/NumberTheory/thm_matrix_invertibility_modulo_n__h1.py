import sympy
from sympy import Matrix, eye, zeros
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a square matrix with integer entries",
    "¬Q: A is invertible modulo n is not equivalent to gcd(det(A), n) == 1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        A, n = witness
    except Exception:
        return [False, False]
        
    # H_1: A is a square matrix with integer entries
    try:
        h1_ok = bool(isinstance(A, sympy.MatrixBase) and A.is_square and all(e.is_integer for e in A))
    except Exception:
        h1_ok = False
        
    # ¬Q: A is invertible modulo n iff gcd(det(A), n) == 1 (must fail)
    try:
        # Check if A is invertible modulo n
        try:
            A.inv_mod(n)
            inv_mod_exists = True
        except Exception:
            inv_mod_exists = False
            
        # Check if gcd(det(A), n) == 1
        det_A = A.det()
        gcd_val = sympy.gcd(det_A, n)
        gcd_is_one = (gcd_val == 1)
        
        # The conclusion is the equivalence of the two statements
        q_ok = (inv_mod_exists == gcd_is_one)
        neg_q = not q_ok
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]