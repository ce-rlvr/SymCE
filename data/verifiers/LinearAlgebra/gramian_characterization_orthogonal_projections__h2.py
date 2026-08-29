import sympy as sp
from sympy import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    """Helper to check if a sympy matrix is exactly zero."""
    if getattr(M, 'is_zero_matrix', False):
        return True
    for val in M:
        if sp.expand(val) != 0 and sp.simplify(val) != 0:
            return False
    return True

def conditions(witness) -> list[bool]:
    # H_1: Let P be a square matrix.
    try:
        if not isinstance(witness, sp.MatrixBase):
            h1 = False
        else:
            h1 = witness.is_square
    except Exception:
        h1 = False

    # ¬Q: The equivalence (P is an orthogonal projection matrix iff P^T P = P) fails.
    # Note: An orthogonal projection matrix is idempotent (P^2 = P) and self-adjoint (P^H = P).
    # For complex matrices, P^T P = P does not necessarily mean P is an orthogonal projection,
    # which makes the conjecture false.
    try:
        if not isinstance(witness, sp.MatrixBase) or not witness.is_square:
            neg_q = False
        else:
            # Check if P is an orthogonal projection (P^2 = P and P^H = P)
            is_idempotent = is_zero_mat(witness * witness - witness)
            is_hermitian = is_zero_mat(witness.H - witness)
            is_ortho_proj = is_idempotent and is_hermitian
            
            # Check if P^T P = P
            pt_p_eq_p = is_zero_mat(witness.T * witness - witness)
            
            # The conjecture claims these two conditions are equivalent
            q = (is_ortho_proj == pt_p_eq_p)
            
            # We want the negated conclusion (the equivalence fails at the witness)
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: P is a square matrix",
    "¬Q: The equivalence (P is an orthogonal projection iff P^T P = P) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1