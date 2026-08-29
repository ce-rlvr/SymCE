import sympy
from sympy import MatrixBase, eye, zeros

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
            # The conclusion states A is similar over the reals to a real Jordan form.
            # If A is similar over the reals to a real matrix, A itself must be real.
            # The Real Jordan Canonical Form Theorem guarantees every real matrix has such a form.
            # Therefore, the conclusion fails if and only if A is not a real matrix.
            is_real = all(e.is_real == True for e in witness)
            neg_q = not is_real
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "¬Q: A is not similar over the real numbers to a real Jordan canonical form"
]

N_HYP = 1
NEG_Q_INDEX = 1