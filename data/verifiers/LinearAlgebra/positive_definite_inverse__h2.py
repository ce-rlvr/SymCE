import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n real symmetric matrix
    try:
        if not getattr(witness, "is_Matrix", False):
            h1 = False
        elif not witness.is_square:
            h1 = False
        elif witness != witness.T:
            h1 = False
        else:
            h1 = True
            for e in witness:
                if not e.is_real:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # ¬Q: A is not invertible or A^{-1} is not positive definite
    try:
        if not getattr(witness, "is_Matrix", False) or not witness.is_square:
            neg_q = False
        elif witness.det() == 0:
            neg_q = True
        else:
            A_inv = witness.inv()
            is_pd = True
            # Sylvester's criterion for positive definiteness
            for i in range(1, A_inv.rows + 1):
                if A_inv[:i, :i].det() <= 0:
                    is_pd = False
                    break
            neg_q = not is_pd
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real symmetric matrix",
    "¬Q: A is not invertible or A^{-1} is not positive definite"
]

N_HYP = 1
NEG_Q_INDEX = 1