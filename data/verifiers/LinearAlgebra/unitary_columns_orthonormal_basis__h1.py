import sympy
from sympy import eye, zeros, simplify

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (U, n) where U is a matrix and n is the dimension of C^n.
    If only U is provided, n defaults to U.cols.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            U, n = witness
        else:
            U = witness
            n = getattr(U, 'cols', None)
            if n is None:
                return [False, False]
    except Exception:
        return [False, False]

    # H_1: Assume U is a unitary matrix.
    try:
        if not getattr(U, 'is_square', False):
            h1 = False
        else:
            diff = U.H * U - eye(U.cols)
            if diff.is_zero_matrix:
                h1 = True
            else:
                h1 = bool(simplify(diff).is_zero_matrix)
    except Exception:
        h1 = False

    # ¬Q: The column vectors of U do not form an orthonormal basis for the complex vector space C^n.
    try:
        # For the columns of U to form a basis for C^n, they must be vectors in C^n
        # (meaning U must have exactly n rows) and there must be exactly n of them
        # (meaning U must have exactly n columns).
        # Since U is unitary (and thus square), U.rows == U.cols.
        # Therefore, they form a basis for C^n if and only if U.cols == n.
        neg_q = bool((U.cols != n) or (U.rows != n))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: The column vectors of U do not form an orthonormal basis for C^n"
]

N_HYP = 1
NEG_Q_INDEX = 1