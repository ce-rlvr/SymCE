import sympy
from sympy import eye, simplify, I, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, MatrixBase) or witness.rows != witness.cols:
            h1 = False
        else:
            n = witness.rows
            diff = witness * witness.H - eye(n)
            h1 = all(simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, MatrixBase) or witness.rows != witness.cols:
            neg_q = False
        else:
            n = witness.rows
            w_conj = witness.conjugate()
            diff = w_conj * w_conj.H - eye(n)
            is_unitary = all(simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
            neg_q = not is_unitary
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: The complex conjugate matrix is not a unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1