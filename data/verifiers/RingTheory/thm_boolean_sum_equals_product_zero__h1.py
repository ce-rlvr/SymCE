import sympy as sp
from sympy.matrices import eye, zeros

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: x and y are elements of R
    # We verify this by checking if they support basic ring operations (addition, multiplication, subtraction)
    try:
        x, y = witness
        _ = x + y
        _ = x * y
        _ = x - x
        _ = y - y
        h1 = True
    except Exception:
        h1 = False

    # H_2: x + y = x * y
    try:
        x, y = witness
        h2 = bool(x + y == x * y)
    except Exception:
        h2 = False

    # ¬Q: not (x = 0 and y = 0)
    # We check if an element is zero by comparing it to its additive identity (x - x)
    try:
        x, y = witness
        x_is_zero = bool(x == x - x)
        y_is_zero = bool(y == y - y)
        neg_q = not (x_is_zero and y_is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of R",
    "H_2: x + y = x * y",
    "¬Q: x != 0 or y != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2