import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (A, A_inv), checks if it satisfies the hypothesis
    but fails the conclusion.
    """
    try:
        A, A_inv = witness
        # Convert to sympy Matrix if not already one (e.g., if lists are provided)
        if not hasattr(A, 'shape') or not hasattr(A, 'H'):
            A = Matrix(A)
        if not hasattr(A_inv, 'shape') or not hasattr(A_inv, 'H'):
            A_inv = Matrix(A_inv)
    except Exception:
        return [False, False]
        
    def is_equal(M1, M2):
        if M1.shape != M2.shape:
            return False
        diff = M1 - M2
        for e in diff:
            if e != 0 and sympy.simplify(e) != 0:
                return False
        return True

    # H_1: A^(1) is a generalized inverse of A satisfying A * A^(1) * A = A
    try:
        if A.shape[1] != A_inv.shape[0] or A.shape[0] != A_inv.shape[1]:
            h1 = False
        else:
            h1 = is_equal(A * A_inv * A, A)
    except Exception:
        h1 = False

    # ¬Q: The matrices AA^(1) and A^(1)A are NOT both idempotent projection operators.
    # In this context, a projection operator implies an orthogonal projection, 
    # which must be both idempotent (P^2 = P) and Hermitian (P^H = P).
    try:
        P1 = A * A_inv
        P2 = A_inv * A
        
        is_P1_proj = is_equal(P1 * P1, P1) and is_equal(P1.H, P1)
        is_P2_proj = is_equal(P2 * P2, P2) and is_equal(P2.H, P2)
        
        neg_q = not (is_P1_proj and is_P2_proj)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A^(1) is a generalized inverse of A satisfying A*A^(1)*A = A",
    "¬Q: AA^(1) and A^(1)A are not both idempotent projection operators (i.e., not both Hermitian and idempotent)"
]

N_HYP = 1
NEG_Q_INDEX = 1