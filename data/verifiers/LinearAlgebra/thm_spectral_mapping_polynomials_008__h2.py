import sympy
from sympy import MatrixBase, Poly, eye, zeros, simplify
from sympy.abc import x
import sympy.matrices
import sympy.polys
import math
import itertools
import functools

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, q, lam = witness
    except Exception:
        return [False, False, False]
        
    # H1: A is an n x n matrix over a field F
    try:
        h1 = isinstance(A, MatrixBase) and A.is_square
    except Exception:
        h1 = False
        
    # H2: q(x) is a polynomial with coefficients in F
    try:
        p = Poly(q, x)
        coeffs = p.all_coeffs()
        # Coefficients should be scalars, not matrices
        if any(isinstance(c, MatrixBase) for c in coeffs):
            h2 = False
        else:
            h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: q(lambda) is NOT an eigenvalue of the matrix q(A)
    try:
        if isinstance(lam, MatrixBase):
            neg_q = False
        else:
            n = A.shape[0]
            p = Poly(q, x)
            coeffs = p.all_coeffs()
            degree = len(coeffs) - 1
            
            # Compute q(A)
            qA = zeros(n, n)
            for i, c in enumerate(coeffs):
                power = degree - i
                qA += c * (A ** power)
                
            # Compute q(lambda)
            q_lam = p.eval(lam)
            
            # Check if q(lambda) is an eigenvalue of q(A)
            # It is an eigenvalue iff det(q(A) - q(lambda)*I) == 0
            I = eye(n)
            char_val = (qA - q_lam * I).det()
            
            try:
                is_zero = char_val.is_zero
            except Exception:
                is_zero = None
                
            if is_zero is not None:
                neg_q = not is_zero
            else:
                neg_q = simplify(char_val) != 0
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: q(x) is a polynomial",
    "¬Q: q(lambda) is not an eigenvalue of q(A)"
]

N_HYP = 2
NEG_Q_INDEX = 2