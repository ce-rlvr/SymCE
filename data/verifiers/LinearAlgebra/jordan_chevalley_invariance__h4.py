import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        T_raw, S_raw, N_raw, W_raw = witness
    except Exception:
        return [False, False, False, False]

    try:
        T = Matrix(T_raw)
        S = Matrix(S_raw)
        N = Matrix(N_raw)
        W = Matrix(W_raw)
    except Exception:
        return [False, False, False, False]

    # H_1: V is a finite-dimensional vector space over a perfect field F
    try:
        h1 = bool(T.shape[0] == W.shape[0])
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V
    try:
        h2 = bool(T.is_square)
    except Exception:
        h2 = False

    # H_3: T = S + N is the unique Jordan-Chevalley decomposition of T, where S is semisimple, N is nilpotent, and S commutes with N
    try:
        if S.shape == T.shape and N.shape == T.shape and T.is_square:
            n = T.shape[0]
            is_decomp = (T == S + N)
            is_semi = S.is_diagonalizable()
            is_nilp = (N**n == zeros(n, n))
            is_comm = (S * N == N * S)
            h3 = bool(is_decomp and is_semi and is_nilp and is_comm)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: W is not invariant under both S and N
    try:
        rank_W = W.rank()
        inv_S = (W.row_join(S * W).rank() == rank_W)
        inv_N = (W.row_join(N * W).rank() == rank_W)
        neg_q = not (inv_S and inv_N)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a perfect field F",
    "H_2: T is a linear operator on V",
    "H_3: T = S + N is the unique Jordan-Chevalley decomposition of T, where S is semisimple, N is nilpotent, and S commutes with N",
    "¬Q: W is not invariant under both S and N"
]

N_HYP = 3
NEG_Q_INDEX = 3