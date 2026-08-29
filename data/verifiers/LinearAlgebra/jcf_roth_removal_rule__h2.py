import sympy
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A and B are square matrices",
    "H_2: C has appropriate dimensions such that the block matrix is well-defined",
    "¬Q: The block matrix is not similar to the block diagonal matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        A, B, C = witness
        # Convert to SymPy matrices if they aren't already
        if not hasattr(A, 'is_square'):
            A = Matrix(A)
        if not hasattr(B, 'is_square'):
            B = Matrix(B)
        if not hasattr(C, 'shape'):
            C = Matrix(C)
    except Exception:
        return [False, False, False]

    try:
        h1 = A.is_square and B.is_square
    except Exception:
        h1 = False

    try:
        h2 = C.shape == (A.shape[0], B.shape[1])
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n = A.shape[0]
            m = B.shape[0]
            
            # Construct the block matrix M = [A, C; 0, B]
            M = Matrix(n + m, n + m, lambda i, j: 
                A[i, j] if i < n and j < n else
                C[i, j - n] if i < n and j >= n else
                0 if i >= n and j < n else
                B[i - n, j - n]
            )
            
            # Construct the block diagonal matrix D = [A, 0; 0, B]
            D = Matrix(n + m, n + m, lambda i, j: 
                A[i, j] if i < n and j < n else
                0 if i < n and j >= n else
                0 if i >= n and j < n else
                B[i - n, j - n]
            )
            
            def get_blocks(J):
                blocks = []
                k = J.shape[0]
                i = 0
                while i < k:
                    val = J[i, i]
                    size = 1
                    # SymPy's jordan_form puts 1s on the superdiagonal
                    while i + size < k and J[i + size - 1, i + size] == 1 and J[i + size, i + size] == val:
                        size += 1
                    blocks.append((val, size))
                    i += size
                # Sort by string representation of eigenvalue, then by block size
                return sorted(blocks, key=lambda x: (str(x[0]), x[1]))
            
            JM = M.jordan_form()[1]
            JD = D.jordan_form()[1]
            
            similar = (get_blocks(JM) == get_blocks(JD))
            neg_q = not similar
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]