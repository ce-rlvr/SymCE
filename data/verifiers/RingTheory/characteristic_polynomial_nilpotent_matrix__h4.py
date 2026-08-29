from sympy import MatrixBase, eye, zeros, Symbol, Expr

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        h2 = h1 and witness.rows > 0
    except Exception:
        h2 = False

    try:
        h3 = h1 and all(isinstance(e, Expr) for e in witness)
    except Exception:
        h3 = False

    try:
        if not h2:
            neg_q = False
        else:
            x = Symbol('x')
            n = witness.rows
            cp = witness.charpoly(x)
            diff = (cp.as_expr() - x**n).simplify()
            neg_q = diff != 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: n is a positive integer (dimension > 0)",
    "H_3: K is a field (entries are valid expressions)",
    "¬Q: The characteristic polynomial of A is not x^n"
]

N_HYP = 3
NEG_Q_INDEX = 3