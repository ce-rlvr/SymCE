import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: V is a vector space (witness is a square matrix)
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H_2: P is a projection operator on V
    try:
        h2 = h1 and bool(witness**2 == witness)
    except Exception:
        h2 = False

    # H_3: P is not the zero operator
    try:
        h3 = h1 and bool(witness != zeros(witness.rows, witness.cols))
    except Exception:
        h3 = False

    # ¬Q: The minimal polynomial of P is not x^2 - x
    try:
        if not h1:
            neg_q = False
        else:
            x = sympy.Symbol('x')
            min_poly = witness.minimal_polynomial(x)
            expected_poly = x**2 - x
            neg_q = bool(sympy.expand(min_poly - expected_poly) != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space (witness is a square matrix)",
    "H_2: P is a projection operator on V",
    "H_3: P is not the zero operator",
    "¬Q: The minimal polynomial of P is not x^2 - x"
]

N_HYP = 3
NEG_Q_INDEX = 3