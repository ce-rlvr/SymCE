import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that the sum of the k largest singular values is always a norm.
    This fails when k = 0, as the sum is 0 for all matrices, violating definiteness.
    """
    try:
        # The witness can be a tuple (A, k) or just the integer k.
        # If only k is provided, we use a dummy non-zero matrix A to test the norm property.
        if isinstance(witness, tuple) and len(witness) == 2:
            A, k = witness
        elif isinstance(witness, int):
            k = witness
            A = sp.Matrix([[1]])
        else:
            A, k = None, None
    except Exception:
        A, k = None, None

    # H1: A is an m x n complex matrix
    try:
        h1 = isinstance(A, sp.MatrixBase)
    except Exception:
        h1 = False

    # H2: k largest singular values of A
    # For the phrase "k largest singular values" to be well-defined, we must have 0 <= k <= min(m, n).
    try:
        h2 = isinstance(k, int) and 0 <= k <= min(A.shape)
    except Exception:
        h2 = False

    # neg_Q: The function ||A||_{(k)} is NOT a unitarily invariant matrix norm.
    # A valid norm must satisfy definiteness: ||A|| == 0 iff A == 0.
    # If A is a non-zero matrix but its k-norm is 0, the function fails to be a norm.
    try:
        if h1 and h2:
            is_zero = A.is_zero_matrix
            if is_zero is None:
                is_zero = all(e == 0 for e in A)
            
            # For k = 0, the sum of the 0 largest singular values is 0.
            # If A is not the zero matrix, this violates definiteness.
            if not is_zero and k == 0:
                neg_q = True
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "H_2: k is an integer and 0 <= k <= min(m, n)",
    "¬Q: The function ||A||_{(k)} is not a valid matrix norm"
]

N_HYP = 2
NEG_Q_INDEX = 2