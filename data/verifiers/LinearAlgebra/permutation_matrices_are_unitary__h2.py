import sympy
from sympy.matrices import MatrixBase, eye, zeros, Matrix

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: P is a square matrix
    try:
        h1 = isinstance(witness, MatrixBase) and witness.shape[0] == witness.shape[1] and witness.shape[0] > 0
    except Exception:
        h1 = False

    # ¬Q: P is not a unitary matrix
    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            prod = witness * witness.H
            if prod == eye(n):
                neg_q = False
            else:
                prod = sympy.expand(prod)
                neg_q = bool(prod != eye(n))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a square matrix",
    "¬Q: P is not a unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1