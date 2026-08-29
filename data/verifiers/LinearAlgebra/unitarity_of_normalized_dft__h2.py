import sympy
from sympy import sqrt, eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            F = witness.get('F')
            U = witness.get('U')
        else:
            n, F, U = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    try:
        if hasattr(U, 'shape') and hasattr(F, 'shape') and U.shape == F.shape:
            diff = (U - F / sympy.sqrt(n)).applyfunc(sympy.simplify)
            h2 = diff == sympy.zeros(*U.shape)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if hasattr(U, 'is_square') and U.is_square:
            prod = U * U.H
            diff = (prod - sympy.eye(U.rows)).applyfunc(sympy.simplify)
            is_unitary = diff == sympy.zeros(*U.shape)
        else:
            is_unitary = False
        neg_q = not is_unitary
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: U = 1/sqrt(n) * F",
    "¬Q: U is not a unitary matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2