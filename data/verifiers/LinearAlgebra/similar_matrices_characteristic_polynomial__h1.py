import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let A and B be similar matrices
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                A, B, P = witness
                if A.is_square and B.is_square and P.is_square and A.shape == B.shape == P.shape:
                    P_inv = P.inv()
                    h1 = (A == P * B * P_inv)
                else:
                    h1 = False
            elif len(witness) == 2:
                A, B = witness
                h1 = A.is_similar(B)
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The characteristic polynomial of A is NOT equal to the characteristic polynomial of B
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            A, B = witness[0], witness[1]
            cp_A = A.charpoly(x).as_expr()
            cp_B = B.charpoly(x).as_expr()
            diff = sympy.simplify(cp_A - cp_B)
            neg_q = (diff != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A and B are similar matrices",
    "¬Q: The characteristic polynomial of A is not equal to the characteristic polynomial of B"
]

N_HYP = 1
NEG_Q_INDEX = 1