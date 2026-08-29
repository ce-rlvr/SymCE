import sympy
from sympy.matrices import MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, MatrixBase):
            neg_q = False
        elif not witness.is_square:
            neg_q = True
        else:
            det_val = sympy.simplify(witness.det())
            neg_q = bool(det_val == 0)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There does not exist a unique unitary matrix U and a unique positive definite Hermitian matrix P such that A = UP"
]

N_HYP = 0
NEG_Q_INDEX = 0