import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            x = witness[-1]
        else:
            x = witness
    except Exception:
        x = witness

    # H_1: Let K be a field.
    try:
        if isinstance(x, sympy.Matrix):
            h1 = True
        elif isinstance(x, (int, float, sympy.Number, sympy.Expr)):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: Let A be a unital K-algebra.
    try:
        if isinstance(x, sympy.Matrix):
            h2 = x.is_square
        elif isinstance(x, (int, float, sympy.Number, sympy.Expr)):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: Assume A is algebraic over K.
    try:
        if isinstance(x, sympy.Matrix):
            h3 = len(x.free_symbols) == 0
        elif isinstance(x, (int, float, sympy.Number)):
            h3 = True
        elif isinstance(x, sympy.Expr):
            h3 = len(x.free_symbols) == 0
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The element x is NOT a unit in A.
    try:
        if isinstance(x, sympy.Matrix):
            if x.is_square:
                neg_q = x.det() == 0
            else:
                neg_q = False
        elif isinstance(x, (int, float, sympy.Number, sympy.Expr)):
            neg_q = sympy.S(x) == 0
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: A is a unital K-algebra",
    "H_3: A is algebraic over K",
    "¬Q: x is not a unit in A"
]

N_HYP = 3
NEG_Q_INDEX = 3