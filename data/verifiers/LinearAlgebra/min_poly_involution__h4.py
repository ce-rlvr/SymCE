import sympy
from sympy.matrices import MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        n = witness.shape[0]
        h2 = bool(witness ** 2 == eye(n))
    except Exception:
        h2 = False

    try:
        n = witness.shape[0]
        h3 = bool(witness != eye(n))
    except Exception:
        h3 = False

    try:
        n = witness.shape[0]
        # The minimal polynomial of T is x^2 - 1 if and only if 
        # T^2 = I, T != I, and T != -I.
        is_minpoly_x2_m1 = bool((witness ** 2 == eye(n)) and (witness != eye(n)) and (witness != -eye(n)))
        neg_q = not is_minpoly_x2_m1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space and T is a linear operator on V",
    "H_2: T^2 = I",
    "H_3: T is not the identity operator",
    "¬Q: The minimal polynomial of T is not x^2 - 1"
]

N_HYP = 3
NEG_Q_INDEX = 3