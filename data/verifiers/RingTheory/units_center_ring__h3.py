import sympy
from sympy import eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square and witness.rows > 0
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = witness.rows
            is_scalar = True
            c = witness[0, 0]
            for i in range(n):
                for j in range(n):
                    if i == j:
                        if witness[i, j] != c:
                            is_scalar = False
                    else:
                        if witness[i, j] != 0:
                            is_scalar = False
            
            det_val = witness.det()
            is_unit_R = bool(det_val != 0)
            is_unit_ZR = is_scalar and is_unit_R
            neg_q = (is_unit_ZR != is_unit_R)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: Z(R) is the center of R",
    "¬Q: u is a unit in R but not a unit in Z(R)"
]

N_HYP = 2
NEG_Q_INDEX = 2