import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        S, T = witness
    except Exception:
        return [False, False, False]

    # H_1: S: V -> W and T: V -> W are linear transformations
    try:
        h1 = isinstance(S, MatrixBase) and isinstance(T, MatrixBase) and S.shape == T.shape
    except Exception:
        h1 = False

    # H_2: rank(S) and rank(T) are finite
    try:
        if h1:
            r_S = S.rank()
            r_T = T.rank()
            # For SymPy matrices, rank is always a finite integer if computable
            h2 = isinstance(r_S, (int, sympy.Integer)) and isinstance(r_T, (int, sympy.Integer))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: rank(S + T) > rank(S) + rank(T)
    try:
        if h1:
            neg_q = (S + T).rank() > S.rank() + T.rank()
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S and T are linear transformations V -> W (matrices of the same shape)",
    "H_2: rank(S) and rank(T) are finite",
    "¬Q: rank(S + T) > rank(S) + rank(T)"
]

N_HYP = 2
NEG_Q_INDEX = 2