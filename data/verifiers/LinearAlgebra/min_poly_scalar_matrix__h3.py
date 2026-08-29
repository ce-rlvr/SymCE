import sympy
from sympy import Symbol, simplify, eye, zeros, Expr
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field (A is a square matrix)",
    "H_2: c is an element of F",
    "¬Q: The minimal polynomial of A is not m(x) = x - c"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            c = witness.get('c')
        elif hasattr(witness, 'A') and hasattr(witness, 'c'):
            A = witness.A
            c = witness.c
        else:
            A, c = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(A, MatrixBase) and A.is_square
    except Exception:
        h1 = False

    try:
        h2 = isinstance(c, (int, float, complex, Expr)) and not isinstance(c, MatrixBase)
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            x_sym = Symbol('x')
            min_poly = A.minimal_polynomial(x_sym)
            expected_poly = x_sym - c
            neg_q = bool(simplify(min_poly - expected_poly) != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]