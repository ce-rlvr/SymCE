import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T^*: V^* \\to V^* is the dual operator of T",
    "¬Q: \\dim(\\ker(T^*)) \\neq \\dim(\\ker(T))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    def get_matrix(w):
        if isinstance(w, Matrix):
            return w
        return Matrix(w)

    try:
        mat = get_matrix(witness)
        h1 = True
    except Exception:
        h1 = False

    try:
        mat = get_matrix(witness)
        h2 = True
    except Exception:
        h2 = False

    try:
        mat = get_matrix(witness)
        dim_ker_T = len(mat.nullspace())
        dim_ker_T_star = len(mat.transpose().nullspace())
        neg_q = bool(dim_ker_T != dim_ker_T_star)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]