import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z, t

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, N = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = bool(A.is_diagonalizable())
    except Exception:
        h1 = False
        
    try:
        h2 = bool(N.is_nilpotent())
    except Exception:
        h2 = False
        
    try:
        h3 = bool(A * N == N * A)
    except Exception:
        h3 = False
        
    try:
        p = bool((A + N).is_diagonalizable())
        q = bool(N.is_zero_matrix)
        neg_q = p != q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is diagonalizable over F",
    "H_2: N is a nilpotent matrix",
    "H_3: A N = N A",
    "¬Q: (A + N is diagonalizable over F) is not equivalent to (N is the zero matrix)"
]

N_HYP = 3
NEG_Q_INDEX = 3