import sympy
from sympy import Matrix, eye, zeros, MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness can be either a tuple (n, U) or just the matrix U.
        if isinstance(witness, tuple) and len(witness) == 2:
            n, U = witness
            # Swap if the order is (U, n)
            if not isinstance(n, (int, sympy.Integer)):
                n, U = U, n
            if not isinstance(U, MatrixBase):
                U = Matrix(U)
        else:
            if not isinstance(witness, MatrixBase):
                U = Matrix(witness)
            else:
                U = witness
            n = U.rows
            
        h1 = bool(isinstance(U, MatrixBase) and U.is_square and U.rows > 0 and n == U.rows and n > 0)
    except Exception:
        h1 = False

    try:
        if h1:
            tr = U.trace()
            try:
                val = float(sympy.Abs(tr).evalf())
            except TypeError:
                val = complex(sympy.Abs(tr).evalf()).real
            neg_q = bool(val > n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n matrix where n is a positive integer",
    "¬Q: The absolute value of the trace of U is strictly greater than n"
]

N_HYP = 1
NEG_Q_INDEX = 1