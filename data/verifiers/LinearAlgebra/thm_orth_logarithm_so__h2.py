import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let Q be a real n x n matrix
    try:
        h1 = isinstance(witness, Matrix) and witness.is_square and all(e.is_real for e in witness)
    except Exception:
        h1 = False

    # H_2: Let the determinant of Q be equal to 1
    try:
        h2 = bool(witness.det() == 1)
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist a real n x n skew-symmetric matrix S such that Q = e^S.
    # The exponential map from the Lie algebra so(n) of real skew-symmetric matrices 
    # is surjective onto the special orthogonal group SO(n).
    # Thus, Q = e^S for some real skew-symmetric S if and only if Q is in SO(n).
    # Given det(Q) = 1, Q is in SO(n) if and only if Q^T Q = I.
    # Therefore, the conclusion fails if and only if Q^T Q != I.
    try:
        n = witness.shape[0]
        neg_q = bool(witness.transpose() * witness != eye(n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is a real n x n matrix",
    "H_2: det(Q) == 1",
    "¬Q: There does not exist a real skew-symmetric S such that Q = e^S (i.e., Q^T Q != I)"
]

N_HYP = 2
NEG_Q_INDEX = 2