import sympy
from sympy import Matrix, zeros, eye
from sympy.matrices import MatrixBase

# Setup named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: F is a field
    # In the context of SymPy, matrices are defined over fields (e.g., rationals, reals, or fraction fields of symbols).
    # We verify that the witness can be interpreted as a matrix.
    try:
        if not isinstance(witness, MatrixBase):
            W = Matrix(witness)
        else:
            W = witness
        h1 = True
    except Exception:
        h1 = False
        W = None

    # H_2: A is an n x n matrix over F
    try:
        h2 = h1 and W.is_square
    except Exception:
        h2 = False

    # ¬Q: A^n is not the zero matrix
    try:
        if h2:
            n = W.shape[0]
            if n == 0:
                neg_q = False
            else:
                W_n = W ** n
                is_zero = True
                for element in W_n:
                    # Fast check first, fallback to simplify for symbolic expressions
                    if element != 0 and sympy.simplify(element) != 0:
                        is_zero = False
                        break
                neg_q = not is_zero
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is an n x n matrix over F",
    "¬Q: A^n is not the zero matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2