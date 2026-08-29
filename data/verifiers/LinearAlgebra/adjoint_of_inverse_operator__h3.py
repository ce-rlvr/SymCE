import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, sympy.matrices.MatrixBase)
    except Exception:
        h1 = False

    try:
        h2 = h1 and witness.is_square
    except Exception:
        h2 = False

    try:
        if not h2:
            neg_q = False
        else:
            T = witness
            T_star = T.H
            try:
                lhs = T_star.inv()
            except Exception:
                # T* is not invertible, so the conclusion fails
                neg_q = True
            else:
                try:
                    rhs = (T.inv()).H
                    conclusion = (lhs == rhs)
                    neg_q = not conclusion
                except Exception:
                    # T is not invertible, so (T^(-1))* is undefined and conclusion fails
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: T is a linear operator on V",
    "¬Q: T* is not invertible or (T*)^(-1) != (T^(-1))*"
]

N_HYP = 2
NEG_Q_INDEX = 2