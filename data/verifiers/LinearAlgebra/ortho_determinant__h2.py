import sympy
from sympy import simplify
from sympy.matrices import eye, zeros, MatrixBase
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Q is an n x n matrix
    try:
        if hasattr(witness, 'shape'):
            r, c = witness.shape
        else:
            r, c = witness.rows, witness.cols
        h1 = bool(r == c)
    except Exception:
        h1 = False

    # H_2: Q is an orthogonal matrix
    try:
        n = witness.shape[0] if hasattr(witness, 'shape') else witness.rows
        I = eye(n)
        QT = witness.T if hasattr(witness, 'T') else witness.transpose()
        QTQ = QT * witness
        
        if QTQ == I:
            h2 = True
        else:
            is_ortho = True
            for i in range(n):
                for j in range(n):
                    val = QTQ[i, j]
                    expected = 1 if i == j else 0
                    if val == expected:
                        continue
                    try:
                        if simplify(val - expected) == 0:
                            continue
                    except Exception:
                        pass
                    is_ortho = False
                    break
                if not is_ortho:
                    break
            h2 = bool(is_ortho)
    except Exception:
        h2 = False

    # ¬Q: The determinant of Q is neither 1 nor -1
    try:
        d = witness.det()
        if d == 1 or d == -1:
            neg_q = False
        else:
            try:
                sd = simplify(d)
                if sd == 1 or sd == -1:
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n matrix",
    "H_2: Q is an orthogonal matrix",
    "¬Q: The determinant of Q is neither 1 nor -1"
]

N_HYP = 2
NEG_Q_INDEX = 2