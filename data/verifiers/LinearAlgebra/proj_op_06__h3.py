import sympy as sp
from sympy.matrices import Matrix, eye, zeros
from sympy import I

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The dropped hypothesis was likely "P is a real matrix". In the real case,
    an orthogonal projection is symmetric (P = P.T). For complex matrices, 
    an orthogonal projection should be Hermitian (P = P.H). By dropping the 
    real hypothesis but keeping the symmetry check for "orthogonal projection", 
    a Hermitian but non-symmetric projection matrix becomes a valid counterexample 
    that has a spectral norm of exactly 1.
    """
    try:
        # H_1: P is a projection matrix (P^2 = P)
        h1 = bool(witness * witness == witness)
    except Exception:
        h1 = False

    try:
        # H_2: P is not an orthogonal projection
        # Evaluated as not symmetric, which is the standard translation 
        # of "not orthogonal projection" from the real-matrix context.
        h2 = not bool(witness.is_symmetric())
    except Exception:
        h2 = False

    try:
        # ¬Q: The spectral norm (induced 2-norm) of P is NOT strictly greater than 1
        # i.e., ||P||_2 <= 1
        norm_val = witness.norm(2)
        neg_q = bool(norm_val <= 1)
    except Exception:
        # Fallback: check if the maximum eigenvalue of P.H * P is <= 1
        try:
            M = witness.H * witness
            evals = M.eigenvals()
            max_eval = max(evals.keys())
            neg_q = bool(max_eval <= 1)
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is a projection matrix",
    "H_2: P is not an orthogonal projection",
    "¬Q: The spectral norm of P is not strictly greater than 1"
]

N_HYP = 2
NEG_Q_INDEX = 2