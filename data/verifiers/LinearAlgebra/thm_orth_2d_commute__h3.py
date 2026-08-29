import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        A = Matrix(witness[0])
        B = Matrix(witness[1])
    except Exception:
        return [False, False, False]

    try:
        if A.shape != (2, 2) or B.shape != (2, 2):
            h1_ok = False
        else:
            real_A = (sympy.conjugate(A) == A)
            real_B = (sympy.conjugate(B) == B)
            ortho_A = sympy.simplify(A * A.T - I2) == O2
            ortho_B = sympy.simplify(B * B.T - I2) == O2
            h1_ok = bool(real_A and real_B and ortho_A and ortho_B)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(sympy.simplify(A.det() - 1) == 0)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = bool(sympy.simplify(A * B - B * A) != O2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A and B are 2x2 real orthogonal matrices",
    "H_2: det(A) == 1",
    "¬Q: AB != BA"
]

N_HYP = 2
NEG_Q_INDEX = 2