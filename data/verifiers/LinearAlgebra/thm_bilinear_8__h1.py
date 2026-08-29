import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    # H_1: B is a symmetric bilinear form on V
    try:
        if hasattr(witness, 'is_symmetric'):
            attr = witness.is_symmetric
            h1 = bool(attr() if callable(attr) else attr)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: B is positive definite (i.e., B(v, v) > 0 for all non-zero v \in V)
    try:
        if hasattr(witness, 'is_positive_definite'):
            attr = witness.is_positive_definite
            h2 = bool(attr() if callable(attr) else attr)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The bilinear form B is degenerate
    try:
        if hasattr(witness, 'is_non_degenerate'):
            attr = witness.is_non_degenerate
            neg_q = not bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'is_degenerate'):
            attr = witness.is_degenerate
            neg_q = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'det'):
            attr = witness.det
            neg_q = (attr() if callable(attr) else attr) == 0
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is a symmetric bilinear form on V",
    "H_2: B is positive definite",
    "¬Q: The bilinear form B is degenerate"
]

N_HYP = 2
NEG_Q_INDEX = 2