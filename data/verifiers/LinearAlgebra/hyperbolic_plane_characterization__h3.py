import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: V is a 2-dimensional vector space over a field of characteristic not 2.
    # We assume the witness is provided as a Gram matrix over Q (characteristic 0).
    try:
        h1 = isinstance(witness, Matrix) and witness.shape == (2, 2)
    except Exception:
        h1 = False

    # H_2: q is a regular quadratic form on V.
    try:
        h2 = witness.is_symmetric() and witness.det() != 0
    except Exception:
        h2 = False

    # ¬Q: The quadratic space V is NOT isometric to the hyperbolic plane.
    # Over Q, a 2D regular quadratic space is a hyperbolic plane iff its determinant is -1 modulo squares.
    # This means -det(witness) must be a square of a rational number for it to be a hyperbolic plane.
    try:
        d = sympy.Rational(-witness.det())
        sq = sympy.sqrt(d)
        # If sq.is_rational is True, it IS isometric to the hyperbolic plane (conclusion holds).
        # We want the negated conclusion, so we negate the boolean.
        neg_q = not bool(sq.is_rational)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a 2-dimensional vector space over a field of characteristic not 2",
    "H_2: q is a regular quadratic form on V",
    "¬Q: V is not isometric to the hyperbolic plane"
]

N_HYP = 2
NEG_Q_INDEX = 2