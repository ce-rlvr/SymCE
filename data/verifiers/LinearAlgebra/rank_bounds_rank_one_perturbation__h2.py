import sympy as sp
from sympy import Matrix, eye, zeros, Rational
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            u = witness.get('u')
            v = witness.get('v')
        else:
            A, u, v = witness
    except Exception:
        return [False, False, False]

    # H1: A is an m x n matrix over a field F
    try:
        h1 = isinstance(A, MatrixBase)
    except Exception:
        h1 = False

    # H2: v is an n x 1 non-zero column vector over F
    try:
        if isinstance(v, MatrixBase) and isinstance(A, MatrixBase):
            n = A.shape[1]
            h2 = (v.shape == (n, 1)) and not v.is_zero_matrix
        else:
            h2 = False
    except Exception:
        h2 = False

    # Conclusion: rank(A) - 1 <= rank(A + uv^T) <= rank(A) + 1
    try:
        rA = A.rank()
        uvT = u * v.T
        A_uvT = A + uvT
        rA_uvT = A_uvT.rank()
        conclusion = (rA - 1 <= rA_uvT) and (rA_uvT <= rA + 1)
    except Exception:
        conclusion = False

    neg_q = not conclusion

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over a field F",
    "H_2: v is an n x 1 non-zero column vector over F",
    "¬Q: rank(A) - 1 <= rank(A + uv^T) <= rank(A) + 1 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2