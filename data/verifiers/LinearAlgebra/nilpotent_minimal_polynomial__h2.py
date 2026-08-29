import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let A be an n x n matrix over a field F
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # ¬Q: The minimal polynomial of A is not x^k
    try:
        if not h1:
            neg_q = False
        else:
            x = sympy.Symbol('x')
            p = sympy.minpoly(witness, x)
            k = sympy.degree(p, x)
            is_xk = (p == x**k)
            neg_q = not is_xk
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "¬Q: The minimal polynomial of A is not of the form x^k"
]

N_HYP = 1
NEG_Q_INDEX = 1