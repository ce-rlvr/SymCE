import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, sympy.MatrixBase):
            M = witness
        else:
            M = sympy.Matrix(witness)
        h1 = True
    except Exception:
        h1 = False

    try:
        if isinstance(witness, sympy.MatrixBase):
            M = witness
        else:
            M = sympy.Matrix(witness)
        neg_q = M.rank() != M.cols
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "¬Q: V^*/W^0 is not naturally isomorphic to W^*"
]

N_HYP = 1
NEG_Q_INDEX = 1