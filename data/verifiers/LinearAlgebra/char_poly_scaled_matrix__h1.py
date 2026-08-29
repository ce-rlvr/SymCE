import sympy
from sympy import Matrix, eye, zeros, Symbol, simplify

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            c = witness.get('c')
            n = witness.get('n')
        else:
            A, c, n = witness
    except Exception:
        return [False, False, False]

    # H_1: A is a square matrix (so its characteristic polynomial is defined)
    try:
        h1 = isinstance(A, sympy.MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # H_2: c is a non-zero scalar
    try:
        if isinstance(c, sympy.MatrixBase):
            h2 = False
        else:
            h2 = bool(c != 0)
    except Exception:
        h2 = False

    # ¬Q: The conclusion p_{cA}(x) = c^n p_A(x/c) FAILS
    try:
        x = Symbol('x')
        p_A = A.charpoly(x).as_expr()
        p_cA = (c * A).charpoly(x).as_expr()
        
        rhs = (c**n) * p_A.subs(x, x/c)
        
        diff = simplify(p_cA - rhs)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: c is a non-zero scalar",
    "¬Q: p_{cA}(x) != c^n p_A(x/c)"
]

N_HYP = 2
NEG_Q_INDEX = 2