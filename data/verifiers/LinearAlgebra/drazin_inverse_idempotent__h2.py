import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_matrix(M):
    """Helper function to robustly check if a SymPy matrix is zero."""
    for e in M:
        e_simp = sp.simplify(e)
        if e_simp == 0:
            continue
        if e_simp.is_number:
            try:
                if abs(complex(e_simp)) < 1e-9:
                    continue
            except Exception:
                pass
        return False
    return True

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    try:
        P = Matrix(witness)
    except Exception:
        return [False, False]
        
    # H_1: P is an idempotent matrix (P^2 = P)
    try:
        if not P.is_square:
            h1 = False
        else:
            h1 = is_zero_matrix(P**2 - P)
    except Exception:
        h1 = False
        
    # ¬Q: The Drazin inverse P^D is not equal to P
    # Mathematically, for any square matrix A, its Drazin inverse A^D equals A 
    # if and only if A^3 = A. Therefore, P^D != P is exactly equivalent to P^3 != P.
    try:
        if not P.is_square:
            neg_q = False
        else:
            neg_q = not is_zero_matrix(P**3 - P)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is an idempotent matrix (P^2 = P)",
    "¬Q: The Drazin inverse P^D is not equal to P"
]

N_HYP = 1
NEG_Q_INDEX = 1