import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_pos_def(M):
    if not M.is_square:
        return False
    if M != M.T:
        return False
    for i in range(1, M.rows + 1):
        if float(M[:i, :i].det()) <= 0:
            return False
    return True

def conditions(witness):
    """
    Given a witness tuple (B1, B2) representing bilinear forms on a real vector space V,
    checks the hypotheses and the negated conclusion.
    """
    try:
        B1, B2 = witness
    except Exception:
        return [False, False, False]

    # H_1: V is a vector space over the real numbers
    # We interpret this as B1 and B2 being real square matrices of the same dimension.
    try:
        h1 = (isinstance(B1, Matrix) and isinstance(B2, Matrix) and 
              B1.is_square and B2.is_square and 
              B1.shape == B2.shape)
        if h1:
            try:
                for e in B1:
                    float(e)
                for e in B2:
                    float(e)
            except Exception:
                h1 = False
    except Exception:
        h1 = False

    # H_2: B_1 is a positive definite bilinear form on V
    try:
        h2 = is_pos_def(B1)
    except Exception:
        h2 = False

    # ¬Q: The sum B_1 + B_2 is NOT a positive definite bilinear form on V
    try:
        B_sum = B1 + B2
        neg_q = not is_pos_def(B_sum)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over the real numbers",
    "H_2: B_1 is a positive definite bilinear form on V",
    "¬Q: The sum B_1 + B_2 is not a positive definite bilinear form on V"
]

N_HYP = 2
NEG_Q_INDEX = 2