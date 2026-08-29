import sympy
from sympy import Matrix, eye, zeros, sympify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: A is a 2x2 matrix over a field F of char != 2 (we use Q)
    try:
        if not hasattr(witness, 'shape') or witness.shape != (2, 2):
            h1 = False
        else:
            h1 = all(sympify(x).is_rational == True for x in witness)
    except Exception:
        h1 = False

    # H2: delta = (a-d)^2 + 4bc != 0
    try:
        a, b, c, d = witness[0, 0], witness[0, 1], witness[1, 0], witness[1, 1]
        delta = (a - d)**2 + 4 * b * c
        h2 = bool(sympify(delta) != 0)
    except Exception:
        h2 = False

    # neg_Q: A is not diagonalizable over F
    # Since delta != 0, A has distinct eigenvalues. It is diagonalizable over Q
    # if and only if all its eigenvalues are in Q.
    try:
        eigenvals = witness.eigenvals()
        all_rational = all(sympify(val).is_rational == True for val in eigenvals.keys())
        neg_q = not all_rational
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a 2x2 matrix over a field F of characteristic != 2 (using Q)",
    "H_2: The discriminant delta = (a-d)^2 + 4bc is non-zero",
    "¬Q: A is not diagonalizable over F"
]

N_HYP = 2
NEG_Q_INDEX = 2