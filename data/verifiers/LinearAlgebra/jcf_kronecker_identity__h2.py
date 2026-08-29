import sympy as sp
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a square complex matrix",
    "¬Q: The Jordan canonical form of A \\otimes I_m does NOT consist of exactly m copies of each Jordan block present in J"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # The witness is expected to be a tuple (A, m) where A is the matrix and m is the size of the identity.
    # If only A is provided, we default m to 2 to evaluate the conclusion.
    if isinstance(witness, tuple):
        if len(witness) == 2:
            A, m = witness
        else:
            return [False, False]
    else:
        A = witness
        m = 2

    # H_1: A is an n x n complex matrix
    try:
        h1 = isinstance(A, sp.Matrix) and A.is_square
    except Exception:
        h1 = False

    # neg_Q: The Jordan canonical form of A \otimes I_m does NOT consist of exactly m copies of each Jordan block present in J
    try:
        if not h1:
            q_holds = True
        else:
            # Extract Jordan blocks of A
            P, J = A.jordan_form()
            blocks_A = []
            n = J.shape[0]
            i = 0
            while i < n:
                val = J[i, i]
                size = 1
                while i + size < n and J[i + size, i + size] == val and J[i + size - 1, i + size] == 1:
                    size += 1
                blocks_A.append((val, size))
                i += size
                
            expected = sorted(blocks_A * m, key=lambda b: (str(b[0]), b[1]))
            
            # Compute Kronecker product A \otimes I_m
            # This will raise an exception if m is invalid (e.g., negative or symbolic),
            # which correctly falsifies the conclusion.
            I_m = sp.eye(m)
            K = sp.kronecker_product(A, I_m)
            
            # Extract Jordan blocks of K
            P_K, J_K = K.jordan_form()
            blocks_K = []
            n_K = J_K.shape[0]
            i = 0
            while i < n_K:
                val = J_K[i, i]
                size = 1
                while i + size < n_K and J_K[i + size, i + size] == val and J_K[i + size - 1, i + size] == 1:
                    size += 1
                blocks_K.append((val, size))
                i += size
                
            actual = sorted(blocks_K, key=lambda b: (str(b[0]), b[1]))
            q_holds = (actual == expected)
    except Exception:
        # If any operation fails (e.g., m is negative and eye(m) fails), the conclusion does not hold.
        q_holds = False

    return [h1, not q_holds]