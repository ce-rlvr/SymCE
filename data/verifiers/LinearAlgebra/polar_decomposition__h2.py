import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The dropped hypothesis was that T is a linear operator on V (i.e., maps V to V).
    Without it, T can be a linear map from V to W (represented by an m x n matrix).
    """
    # H_1: V is a finite-dimensional inner product space
    # We interpret this as the witness being a matrix representing a linear map from V.
    try:
        h1 = isinstance(witness, sympy.MatrixBase)
    except Exception:
        h1 = False

    # ¬Q: The conclusion FAILS at the witness.
    # Conclusion: There exists an isometry S and a unique positive semi-definite operator P such that T = SP.
    # For a matrix T of size m x n (mapping C^n to C^m), an isometry S from C^n to C^m requires m >= n.
    # If m < n, no such isometry S can exist (an isometry must be injective).
    # If m >= n, S always exists and P is always unique (P = sqrt(T^* T)).
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = bool(witness.rows < witness.cols)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "¬Q: There does not exist an isometry S and a unique positive semi-definite operator P such that T = SP"
]

N_HYP = 1
NEG_Q_INDEX = 1