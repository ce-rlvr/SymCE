import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple of three matrices: (T, B, T_star)
        T = Matrix(witness[0])
        B = Matrix(witness[1])
        T_star = Matrix(witness[2])
    except Exception:
        return [False, False, False, False]

    # H_1: V is a finite-dimensional vector space over a field F
    try:
        h1 = bool(T.is_square and B.is_square and T_star.is_square and 
                  T.shape == B.shape == T_star.shape)
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H_3: T^* is the adjoint of T with respect to B
    # The adjoint T^* with respect to a bilinear form B satisfies: B(Tx, y) = B(x, T^*y)
    # In matrix notation: T^T * B = B * T^*
    try:
        h3 = h1 and bool(T.transpose() * B == B * T_star)
    except Exception:
        h3 = False

    # ¬Q: The rank of T is not equal to the rank of T^*
    try:
        neg_q = h1 and bool(T.rank() != T_star.rank())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T is a linear operator on V",
    "H_3: T^* is the adjoint of T with respect to B",
    "¬Q: The rank of T is not equal to the rank of T^*"
]

N_HYP = 3
NEG_Q_INDEX = 3