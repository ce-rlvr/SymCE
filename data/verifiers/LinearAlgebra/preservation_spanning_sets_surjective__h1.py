import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        M_raw, S_raw = witness
        M = Matrix(M_raw)
        S = [Matrix(v) for v in S_raw]
    except Exception:
        return [False, False, False, False]

    # H_1: T is a linear map from V to W
    try:
        h1 = all(v.shape == (M.cols, 1) for v in S)
    except Exception:
        h1 = False

    # H_2: T is surjective
    try:
        h2 = M.rank() == M.rows
    except Exception:
        h2 = False

    # H_3: S is a subset of V that spans V
    try:
        if not S:
            h3 = (M.cols == 0)
        else:
            S_mat = Matrix.hstack(*S)
            h3 = S_mat.rank() == M.cols
    except Exception:
        h3 = False

    # neg_Q: The image T(S) is not a spanning set for W
    try:
        if not S:
            neg_q = (M.rows > 0)
        else:
            TS = [M * v for v in S]
            TS_mat = Matrix.hstack(*TS)
            neg_q = TS_mat.rank() < M.rows
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear map from V to W",
    "H_2: T is surjective",
    "H_3: S is a subset of V that spans V",
    "¬Q: The image T(S) is not a spanning set for W"
]

N_HYP = 3
NEG_Q_INDEX = 3