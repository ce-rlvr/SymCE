import sympy
from sympy import Matrix, eye, zeros
import math

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n real matrix
    try:
        A = sympy.Matrix(witness)
        h1 = A.is_square and all(e.is_real for e in A)
    except Exception:
        h1 = False

    # H_2: All entries of A are non-negative
    try:
        A = sympy.Matrix(witness)
        h2 = all(e >= 0 for e in A)
    except Exception:
        h2 = False

    # neg_Q: 1 is not an eigenvalue of A, or there is a complex eigenvalue lambda with |lambda| > 1
    try:
        A = sympy.Matrix(witness)
        n = A.shape[0]
        
        # Check if 1 is an eigenvalue by evaluating det(A - I) == 0
        det_val = (A - sympy.eye(n)).det()
        try:
            is_one_eigenvalue = abs(complex(det_val)) < 1e-9
        except Exception:
            is_one_eigenvalue = (det_val == 0) or (det_val.is_zero == True)
            
        # Check if any eigenvalue has magnitude > 1
        has_large_eigenvalue = False
        lam = sympy.Symbol('lambda')
        cp = A.charpoly(lam)
        roots = sympy.nroots(cp.as_expr())
        
        for r in roots:
            if abs(complex(r)) > 1.0 + 1e-9:
                has_large_eigenvalue = True
                break
                
        neg_q = (not is_one_eigenvalue) or has_large_eigenvalue
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a square real matrix",
    "H_2: All entries of A are non-negative",
    "¬Q: 1 is not an eigenvalue of A, or A has a complex eigenvalue with magnitude > 1"
]

N_HYP = 2
NEG_Q_INDEX = 2