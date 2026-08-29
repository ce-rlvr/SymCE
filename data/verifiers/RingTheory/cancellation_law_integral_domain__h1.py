import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False, False]

    # H_1: a, b, c are elements of R
    try:
        _ = a * b
        _ = a * c
        _ = b - c
        _ = a - a
        h1 = True
    except Exception:
        h1 = False

    # H_2: a is not equal to 0
    try:
        zero_a = a - a
        if isinstance(a, sympy.Expr) and isinstance(zero_a, sympy.Expr):
            h2 = bool(sympy.simplify(a - zero_a) != 0)
        else:
            h2 = bool(a != zero_a)
    except Exception:
        h2 = False

    # H_3: ab = ac
    try:
        ab = a * b
        ac = a * c
        if isinstance(ab, sympy.Expr) and isinstance(ac, sympy.Expr):
            h3 = bool(sympy.simplify(ab - ac) == 0)
        else:
            h3 = bool(ab == ac)
    except Exception:
        h3 = False

    # ¬Q: b != c
    try:
        if isinstance(b, sympy.Expr) and isinstance(c, sympy.Expr):
            neg_q = bool(sympy.simplify(b - c) != 0)
        else:
            neg_q = bool(b != c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are elements of R",
    "H_2: a is not equal to 0",
    "H_3: ab = ac",
    "¬Q: b != c"
]

N_HYP = 3
NEG_Q_INDEX = 3