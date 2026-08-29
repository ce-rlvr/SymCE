import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let A be an n x n matrix over a field F
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # neg_Q: The minimal polynomial of A is NOT equal to the characteristic polynomial of A
    try:
        if not h1:
            neg_q = False
        else:
            x = sympy.Symbol('x')
            char_poly = witness.charpoly(x).as_expr()
            
            # SymPy's Matrix.minpoly() computes the minimal polynomial
            # It returns a PurePoly, but we can use as_expr() or just compare
            # However, in some versions it might return an expression.
            # We'll convert both to expressions and simplify their difference.
            min_poly = witness.minpoly(x)
            if hasattr(min_poly, 'as_expr'):
                min_poly = min_poly.as_expr()
                
            diff = sympy.simplify(char_poly - min_poly)
            neg_q = (diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The minimal polynomial of A is not equal to the characteristic polynomial of A"
]

N_HYP = 1
NEG_Q_INDEX = 1