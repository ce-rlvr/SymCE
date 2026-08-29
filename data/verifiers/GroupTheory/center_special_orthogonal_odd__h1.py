import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: n is a positive integer (degree of SO(n, R))
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and witness >= 1
    except Exception:
        h1 = False

    # ¬Q: The center of SO(n, R) is NOT the trivial group.
    # For SO(n, R), the center is trivial if n is odd.
    # If n is even, the center contains at least {I, -I} (and is the whole group for n=2),
    # so it is not trivial.
    try:
        neg_q = isinstance(witness, (int, sympy.Integer)) and witness >= 1 and witness % 2 == 0
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The center of SO(n, R) is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1