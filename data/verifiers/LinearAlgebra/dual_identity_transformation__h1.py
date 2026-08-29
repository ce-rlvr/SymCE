import sympy
from sympy import eye, zeros, Matrix

# Top-level setup for Linear Algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the hypotheses and the negated conclusion.
    The witness is expected to be a matrix representing the linear transformation.
    """
    # H_1: I_V is the identity linear transformation on V
    try:
        h1 = False
        if getattr(witness, 'is_Identity', False):
            h1 = True
        elif getattr(witness, 'is_square', False):
            if witness == eye(witness.shape[0]):
                h1 = True
    except Exception:
        h1 = False

    # ¬Q: The dual transformation (I_V)* is not the identity transformation on V*
    try:
        q = False
        if hasattr(witness, 'transpose'):
            dual = witness.transpose()
            if getattr(dual, 'is_Identity', False):
                q = True
            elif getattr(dual, 'is_square', False):
                if dual == eye(dual.shape[0]):
                    q = True
        neg_q = not q
    except Exception:
        # If we cannot compute the dual or check it, we conservatively return False
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I_V is the identity linear transformation on V",
    "¬Q: The dual transformation (I_V)* is not the identity transformation on V*"
]

N_HYP = 1
NEG_Q_INDEX = 1