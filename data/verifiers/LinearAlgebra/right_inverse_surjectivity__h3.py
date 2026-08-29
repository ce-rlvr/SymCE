import sympy
from sympy.matrices import MatrixBase, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # A SymPy matrix implicitly represents a linear map between vector spaces F^n and F^m
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    try:
        # A SymPy matrix implicitly represents a linear map
        h2 = isinstance(witness, MatrixBase)
    except Exception:
        h2 = False

    try:
        # The conclusion states there exists a right inverse S such that T * S = I_W.
        # This is true if and only if T is surjective, which means its rank equals the number of rows (m).
        # The negated conclusion is that no such S exists, meaning T is not surjective (rank < m).
        m = witness.shape[0]
        neg_q = bool(witness.rank() < m)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: T: V -> W is a linear map",
    "¬Q: There does not exist a linear map S: W -> V such that T ∘ S = I_W"
]

N_HYP = 2
NEG_Q_INDEX = 2