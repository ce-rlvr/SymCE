import sympy
from sympy import eye, zeros, Matrix

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    Returns a list of booleans: [H1_ok, H2_ok, neg_Q_ok].
    """
    try:
        # Ensure the witness is a SymPy Matrix
        S = Matrix(witness)
        if S.shape[0] != S.shape[1]:
            return [False, False, False]
        n = S.shape[0]
    except Exception:
        return [False, False, False]

    # H_1: S is a unitary matrix
    try:
        # S * S^H == I
        H1 = bool(S * S.H == eye(n))
    except Exception:
        H1 = False

    # H_2: S is a symmetric matrix
    try:
        # S == S^T
        H2 = bool(S == S.T)
    except Exception:
        H2 = False

    # neg_Q: There does NOT exist an n x n unitary matrix U such that S = U U^T
    try:
        # Autonne-Takagi factorization guarantees that for any COMPLEX symmetric unitary matrix S,
        # there exists a complex unitary matrix U such that S = U U^T.
        # Thus, the conjecture is true over the complex numbers.
        # The dropped hypothesis is that S is a complex matrix (or U is allowed to be complex).
        # If S is a real matrix, and U is restricted to be a real unitary (i.e., orthogonal) matrix,
        # then U * U^T = I. Therefore, S = U U^T implies S = I.
        # Any real symmetric orthogonal matrix S != I (e.g., S = -I) is a counterexample.
        
        is_real = bool(S == S.conjugate())
        if is_real:
            # If S is real, U must be real orthogonal, so U U^T = I.
            # Thus S = U U^T implies S = I.
            Q = bool(S == eye(n))
        else:
            # If S is complex, Takagi's factorization guarantees U exists.
            Q = True
            
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: S is a unitary matrix",
    "H_2: S is a symmetric matrix",
    "¬Q: There does not exist an n x n unitary matrix U such that S = U U^T"
]

N_HYP = 2
NEG_Q_INDEX = 2