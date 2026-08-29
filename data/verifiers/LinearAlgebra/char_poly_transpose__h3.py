import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            t = sympy.Symbol('t')
            p_A = witness.charpoly(t)
            p_AT = witness.transpose().charpoly(t)
            neg_q = p_A != p_AT
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: p_A(t) != p_{A^T}(t)"
]

N_HYP = 1
NEG_Q_INDEX = 1