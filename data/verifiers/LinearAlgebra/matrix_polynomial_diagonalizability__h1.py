import sympy
from sympy import Symbol, Matrix, eye, zeros, Poly
from sympy.matrices import MatrixBase

# Top-level setup
x = Symbol('x')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (A, p) where A is a matrix and p is a polynomial in x,
    checks if it is a valid counterexample to the false conjecture:
    "If p(x) is a polynomial, then p(A) is diagonalizable."
    """
    # H_1: p(x) is a polynomial and A is a square matrix
    try:
        A, p = witness
        if not isinstance(A, MatrixBase) or not A.is_square:
            h1 = False
        else:
            # This will raise an exception if p is not a polynomial in x
            poly = Poly(p, x)
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: p(A) is not diagonalizable
    try:
        A, p = witness
        poly = Poly(p, x)
        coeffs = poly.all_coeffs()
        n = A.shape[0]
        pA = zeros(n, n)
        deg = len(coeffs) - 1
        
        # Evaluate the matrix polynomial p(A)
        for i, c in enumerate(coeffs):
            pA += c * (A ** (deg - i))
            
        # The conclusion is that p(A) is diagonalizable.
        # We want the negation: p(A) is NOT diagonalizable.
        neg_q = not pA.is_diagonalizable()
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p(x) is a polynomial and A is a square matrix",
    "¬Q: p(A) is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1