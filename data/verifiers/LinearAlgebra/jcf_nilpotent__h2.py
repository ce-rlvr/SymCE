import sympy
from sympy.matrices import MatrixBase, zeros, eye

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            N = witness.get('N')
            k = witness.get('k')
        else:
            N, k = witness
            
        if not isinstance(N, MatrixBase):
            N = sympy.Matrix(N)
    except Exception:
        return [False, False]

    # H_1: N is a nilpotent matrix over a field F
    try:
        if not N.is_square:
            h1 = False
        else:
            n = N.shape[0]
            if n == 0:
                h1 = True
            else:
                h1 = bool(N**n == zeros(n, n))
    except Exception:
        h1 = False

    # ¬Q: The Jordan canonical form of N consists entirely of Jordan blocks with eigenvalue 0, 
    # and the maximum size among these blocks is exactly k.
    # Negation: It does NOT consist entirely of Jordan blocks with eigenvalue 0, 
    # OR the maximum size among these blocks is NOT exactly k.
    try:
        if not N.is_square:
            neg_q = False
        else:
            n = N.shape[0]
            if n == 0:
                neg_q = bool(k != 0)
            else:
                if N**n != zeros(n, n):
                    # Not nilpotent -> has non-zero eigenvalues -> conclusion fails
                    neg_q = True
                else:
                    # Nilpotent -> all eigenvalues are 0
                    # Maximum size of Jordan block is the index of nilpotency
                    idx = 1
                    M = N
                    zero_mat = zeros(n, n)
                    while M != zero_mat:
                        M = M * N
                        idx += 1
                    neg_q = bool(idx != k)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a nilpotent matrix over a field F",
    "¬Q: The maximum size of Jordan blocks with eigenvalue 0 is not exactly k, or there are non-zero eigenvalues"
]

N_HYP = 1
NEG_Q_INDEX = 1