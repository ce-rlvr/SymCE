import sympy
from sympy import eye, zeros, expand, simplify

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        # Check if witness is a square matrix
        if hasattr(witness, 'is_square') and witness.is_square and hasattr(witness, 'shape'):
            # Check if all elements are explicitly real
            if all(getattr(elem, 'is_real', None) == True for elem in witness):
                h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if hasattr(witness, 'is_square') and witness.is_square and hasattr(witness, 'shape') and hasattr(witness, 'T'):
            n = witness.shape[0]
            # A real square matrix has all singular values equal to 1 iff Q^T * Q == I
            # The negated conclusion is that Q^T * Q != I
            diff = expand(witness.T * witness - eye(n))
            is_zero = getattr(diff, 'is_zero_matrix', False)
            if not is_zero:
                # Fallback to simplify in case of symbolic entries
                diff = simplify(diff)
                is_zero = getattr(diff, 'is_zero_matrix', False)
            neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "¬Q: Not all singular values of Q are equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1