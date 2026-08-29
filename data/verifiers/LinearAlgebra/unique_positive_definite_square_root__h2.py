import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is a real symmetric n x n matrix
    try:
        if not isinstance(witness, MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        elif witness.shape[0] < 1:
            h1 = False
        elif witness != witness.T:
            h1 = False
        else:
            h1 = all(x.is_real == True for x in witness)
    except Exception:
        h1 = False

    # neg_Q: It is not the case that there exists a unique real symmetric positive definite matrix B such that B^2 = A
    try:
        if not isinstance(witness, MatrixBase) or not witness.is_square or witness.shape[0] < 1 or witness != witness.T or not all(x.is_real == True for x in witness):
            neg_q = True
        else:
            n = witness.shape[0]
            is_pos_def = True
            # Sylvester's criterion for positive definiteness
            for i in range(1, n + 1):
                if witness[:i, :i].det() <= 0:
                    is_pos_def = False
                    break
            neg_q = not is_pos_def
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a real symmetric n x n matrix",
    "¬Q: A does not have a unique real symmetric positive definite square root"
]

N_HYP = 1
NEG_Q_INDEX = 1