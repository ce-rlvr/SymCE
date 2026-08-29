import sympy
from sympy import eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square:
            h1 = False
        else:
            n = witness.shape[0]
            diff1 = sympy.expand(witness.T * witness - eye(n))
            if not all(diff1[i, j] == 0 for i in range(n) for j in range(n)):
                diff1 = sympy.simplify(diff1)
            diff2 = sympy.expand(witness * witness.T - eye(n))
            if not all(diff2[i, j] == 0 for i in range(n) for j in range(n)):
                diff2 = sympy.simplify(diff2)
            
            h1 = all(diff1[i, j] == 0 for i in range(n) for j in range(n)) and \
                 all(diff2[i, j] == 0 for i in range(n) for j in range(n))
    except Exception:
        h1 = False

    try:
        if not hasattr(witness, 'is_diagonalizable'):
            neg_q = False
        else:
            neg_q = not witness.is_diagonalizable()
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an orthogonal matrix",
    "¬Q: A is not diagonalizable over the field of complex numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1