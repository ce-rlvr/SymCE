import sympy
from sympy.polys.constructor import construct_domain
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A = sympy.Matrix(witness)
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a principal ideal domain
    try:
        flat = list(A)
        domain, _ = construct_domain(flat)
        h1 = bool(domain.is_PID)
    except Exception:
        h1 = False
        
    # H2: n is a positive integer
    try:
        if A.is_square:
            n = A.shape[0]
            h2 = bool(n > 0)
        else:
            h2 = False
            n = 0
    except Exception:
        h2 = False
        n = 0
        
    # H3: A^2 = A
    try:
        h3 = bool(A**2 == A)
    except Exception:
        h3 = False
        
    # neg_Q: A is NOT similar over R to a diagonal matrix whose diagonal entries are exclusively 1s and 0s
    try:
        if not h2:
            neg_q = False
        elif A**2 != A:
            # If A is not idempotent, it cannot be similar to a diagonal matrix of 1s and 0s
            # (since similarity preserves idempotence).
            neg_q = True
        else:
            # A is idempotent.
            # Theorem: Over any Principal Ideal Domain, every idempotent matrix is diagonalizable.
            # Thus, if R is a PID, A is guaranteed to be similar to a diagonal matrix of 1s and 0s.
            if h1:
                neg_q = False
            else:
                # Fallback for non-PIDs: check if the nullspaces of A and A-I span R^n
                I = sympy.eye(n)
                null_A = A.nullspace()
                null_A_I = (A - I).nullspace()
                P_cols = null_A_I + null_A
                if len(P_cols) == n:
                    P = sympy.Matrix.hstack(*P_cols)
                    det_P = P.det()
                    if domain.is_unit(det_P):
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: n is a positive integer",
    "H_3: A^2 = A",
    "¬Q: A is not similar over R to a diagonal matrix whose diagonal entries are exclusively 1s and 0s"
]

N_HYP = 3
NEG_Q_INDEX = 3