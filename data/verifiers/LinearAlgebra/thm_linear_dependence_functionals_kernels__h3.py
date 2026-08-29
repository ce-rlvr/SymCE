import sympy
from sympy import Matrix, zeros, eye
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        n, f, F_list = witness
    except Exception:
        return [False, False, False]

    # H_1: V is a vector space over a field F
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H_2: f, f_1, ..., f_k are linear functionals on V
    try:
        f_mat = Matrix(1, n, list(f))
        if not isinstance(F_list, (list, tuple)):
            h2 = False
        else:
            h2 = all(len(list(fi)) == n for fi in F_list)
            if h2:
                if len(F_list) == 0:
                    M = zeros(0, n)
                else:
                    M = Matrix([list(fi) for fi in F_list])
    except Exception:
        h2 = False

    # ¬Q: f is not a linear combination of f_1, ..., f_k
    try:
        if h1 and h2:
            M_aug = M.col_join(f_mat)
            neg_q = M.rank() < M_aug.rank()
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: f, f_1, ..., f_k are linear functionals on V",
    "¬Q: f is not a linear combination of f_1, ..., f_k"
]

N_HYP = 2
NEG_Q_INDEX = 2