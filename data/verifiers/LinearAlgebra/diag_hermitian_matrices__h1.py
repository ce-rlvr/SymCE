import sympy
from sympy import Matrix, eye, zeros, I, Symbol, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is equal to its conjugate transpose (A = A^*)
    try:
        h1 = bool(witness == witness.H)
    except Exception:
        h1 = False

    # ¬Q: A is not diagonalizable over the complex numbers
    try:
        neg_q = not bool(witness.is_diagonalizable())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is equal to its conjugate transpose (A = A^*)",
    "¬Q: A is not diagonalizable over the complex numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1