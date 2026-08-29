import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
        if not isinstance(A, Matrix):
            A = Matrix(A)
        if not isinstance(B, Matrix):
            B = Matrix(B)
    except Exception:
        return [False, False, False]
    
    # H1: A is symmetric and positive definite
    try:
        h1 = False
        if hasattr(A, 'is_square') and A.is_square and A.is_symmetric():
            evs = A.eigenvals()
            is_pd = True
            for ev in evs:
                val = complex(ev.evalf())
                if abs(val.imag) > 1e-9 or val.real <= 1e-9:
                    is_pd = False
                    break
            h1 = is_pd
    except Exception:
        h1 = False

    # H2: B is symmetric
    try:
        h2 = False
        if hasattr(B, 'is_square') and B.is_square and B.is_symmetric():
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: AB is not diagonalizable over the real numbers
    try:
        neg_q = False
        AB = A * B
        if hasattr(AB, 'is_square') and AB.is_square:
            evs = AB.eigenvals()
            all_real = True
            for ev in evs:
                val = complex(ev.evalf())
                if abs(val.imag) > 1e-9:
                    all_real = False
                    break
            
            if all_real:
                is_diag = AB.is_diagonalizable()
                if is_diag == True:
                    neg_q = False
                else:
                    neg_q = True
            else:
                neg_q = True
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is symmetric and positive definite",
    "H_2: B is symmetric",
    "¬Q: The product A B is not diagonalizable over the real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2