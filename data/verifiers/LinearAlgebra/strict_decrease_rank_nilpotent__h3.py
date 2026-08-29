import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: V is an n-dimensional vector space (T is a square matrix)",
    "H_2: T is a nilpotent linear operator",
    "¬Q: rank(T^{k+1}) >= rank(T^k)"
]

def conditions(witness):
    # Unpack witness. It can be a tuple/list (T, k) or just the matrix T.
    # If k is not provided, we default to k = n (the dimension of T), 
    # since for a nilpotent matrix T, T^n = 0, which guarantees rank(T^{n+1}) = rank(T^n) = 0.
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            T, k = witness
            k = int(k)
        else:
            T = witness
            k = getattr(T, 'shape', (0, 0))[0]
    except Exception:
        T = None
        k = 0

    # H_1: V is an n-dimensional vector space (T is a square matrix)
    try:
        h1_ok = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1_ok = False

    # H_2: T is a nilpotent linear operator
    try:
        h2_ok = False
        if h1_ok:
            h2_ok = bool(T.is_nilpotent())
    except Exception:
        h2_ok = False

    # ¬Q: rank(T^{k+1}) >= rank(T^k)
    try:
        neg_q_ok = False
        if h1_ok and k >= 0:
            rk = (T**k).rank()
            rk_plus_1 = (T**(k+1)).rank()
            neg_q_ok = bool(rk_plus_1 >= rk)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]