import sympy
from sympy.matrices import MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            is_diag = bool(witness.is_diagonalizable())
            tr = witness.trace()
            if hasattr(tr, 'is_zero') and tr.is_zero is not None:
                trace_nonzero = not tr.is_zero
            else:
                trace_nonzero = bool(tr != 0)
            neg_q = (is_diag != trace_nonzero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: A is diagonalizable is not equivalent to trace(A) != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1