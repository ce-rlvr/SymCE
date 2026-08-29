import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z
import z3

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Extract the element 'a' if the witness is provided as a tuple (R, a)
    a = witness
    try:
        _ = a + a
        _ = a * a
        _ = a - a
    except Exception:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            a = witness[1]

    # H_1: a is an element of R
    # We verify this by checking if 'a' supports basic ring operations
    try:
        _ = a + a
        _ = a * a
        _ = a - a
        h1 = True
    except Exception:
        h1 = False

    # ¬Q: L_a o L_a != L_a
    # In any ring, L_a(L_a(x)) = a*(a*x) = a^2 * x. 
    # For standard witness objects (which typically belong to rings with identity),
    # L_a o L_a = L_a is equivalent to a^2 = a.
    # We check if a * a != a.
    try:
        if z3.is_expr(a):
            neg_q = bool(z3.is_true(z3.simplify(a * a != a)))
        elif isinstance(a, sympy.Expr):
            neg_q = bool(sympy.simplify(a * a - a) != 0)
        elif isinstance(a, sympy.MatrixBase):
            neg_q = bool(a * a != a)
        else:
            neg_q = bool(a * a != a)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of R",
    "¬Q: L_a o L_a != L_a"
]

N_HYP = 1
NEG_Q_INDEX = 1