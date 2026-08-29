import sympy
from sympy.matrices import MatrixBase
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    try:
        if not h2:
            neg_q = False
        else:
            diag = witness.is_diagonalizable()
            if not diag:
                neg_q = True
            else:
                evs = witness.eigenvals().keys()
                subset_01 = True
                for ev in evs:
                    if ev != 0 and ev != 1:
                        subset_01 = False
                        break
                neg_q = not subset_01
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: P: V \\to V is a linear operator",
    "¬Q: P is not diagonalizable or the spectrum of P is not a subset of {0, 1}"
]

N_HYP = 2
NEG_Q_INDEX = 2