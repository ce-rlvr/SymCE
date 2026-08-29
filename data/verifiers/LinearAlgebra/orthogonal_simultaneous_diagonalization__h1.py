import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple of two matrices (A, B).
    """
    try:
        A, B = witness
    except Exception:
        return [False, False]
    
    # H_1: A and B commute (AB = BA)
    # We also enforce that they are square matrices of the same size.
    try:
        h1 = bool(hasattr(A, 'is_square') and A.is_square and 
                  hasattr(B, 'is_square') and B.is_square and 
                  A.shape == B.shape and 
                  A * B == B * A)
    except Exception:
        h1 = False

    # ¬Q: The conclusion states there exists a real orthogonal matrix Q such that 
    # Q^T A Q and Q^T B Q are diagonal.
    # If such Q exists, then A = Q D_A Q^T. Since D_A is diagonal, D_A^T = D_A.
    # Thus A^T = (Q D_A Q^T)^T = Q D_A^T Q^T = Q D_A Q^T = A.
    # So A and B must be symmetric.
    # Also, since D_A and D_B are diagonal, they commute, which implies A and B commute.
    # Therefore, the conclusion holds iff A and B are symmetric and commute.
    # The negated conclusion is True if this is NOT the case.
    try:
        q_holds = bool((A == A.T) and (B == B.T) and (A * B == B * A))
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B commute (AB = BA)",
    "¬Q: A and B are not simultaneously orthogonally diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1