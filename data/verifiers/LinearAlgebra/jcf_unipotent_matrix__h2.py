import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            x = sympy.Dummy('x')
            char_poly = witness.charpoly(x).as_expr()
            n = witness.shape[0]
            expected_poly = (x - 1)**n
            diff = sympy.simplify(sympy.expand(char_poly - expected_poly))
            neg_q = diff != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is an n x n matrix over C",
    "¬Q: U has at least one Jordan block with an eigenvalue other than 1"
]

N_HYP = 1
NEG_Q_INDEX = 1