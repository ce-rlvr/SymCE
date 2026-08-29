import sympy
from sympy import Matrix, eye, zeros, simplify
from sympy.matrices import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: P is an n x n projection matrix
    try:
        P, c = witness
        h1 = False
        if hasattr(P, 'shape') and len(P.shape) == 2 and P.shape[0] == P.shape[1]:
            n = P.shape[0]
            diff = P * P - P
            is_proj = True
            for i in range(n):
                for j in range(n):
                    if simplify(diff[i, j]) != 0:
                        is_proj = False
                        break
                if not is_proj:
                    break
            h1 = is_proj
    except Exception:
        h1 = False

    # H_2: c is not equal to 1
    try:
        P, c = witness
        h2 = bool(c != 1)
    except Exception:
        h2 = False

    # ¬Q: The matrix I - cP is not invertible, or its inverse is not I + (c / (1 - c))P
    try:
        P, c = witness
        n = P.shape[0]
        I = eye(n)
        
        M = I - c * P
        
        # Check if M is invertible
        d = simplify(M.det())
        if d == 0:
            neg_q = True
        else:
            # Calculate the inverse formula
            # If c is a matrix (counterexample to dropped "c is a scalar" hypothesis),
            # 1 - c or c / (1 - c) will raise a TypeError/Exception in sympy.
            denom = 1 - c
            term = c / denom
            invM_formula = I + term * P
            
            # Verify if it is indeed the inverse
            prod1 = simplify(M * invM_formula)
            prod2 = simplify(invM_formula * M)
            
            if prod1 != I or prod2 != I:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        # If any operation fails (e.g., invalid matrix operations, division by zero),
        # the conclusion fails to hold at the witness.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is an n x n projection matrix",
    "H_2: c is not equal to 1",
    "¬Q: The matrix I - cP is not invertible, or its inverse is not I + (c / (1 - c))P"
]

N_HYP = 2
NEG_Q_INDEX = 2