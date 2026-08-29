import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x

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
            n = witness.rows
            charpoly = witness.charpoly(x).as_expr()
            prod = 1
            for i in range(n):
                prod *= (x - witness[i, i])
            neg_q = bool(sympy.expand(charpoly - prod) != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The characteristic polynomial of A is not \\prod_{i=1}^n (x - A_{ii})"
]

N_HYP = 1
NEG_Q_INDEX = 1