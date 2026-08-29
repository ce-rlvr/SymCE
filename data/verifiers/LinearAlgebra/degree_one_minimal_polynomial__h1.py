import sympy
from sympy import Symbol, MatrixBase, eye, Poly
from sympy.polys import minpoly

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # Attempt to convert block or implicit matrices to explicit matrices
    try:
        if hasattr(witness, 'as_explicit'):
            witness = witness.as_explicit()
    except Exception:
        pass

    # H_1: The minimal polynomial of A has a degree of exactly 1
    h1_ok = False
    x = Symbol('x')
    try:
        if hasattr(witness, 'minimal_polynomial'):
            mp = witness.minimal_polynomial(x)
            if Poly(mp, x).degree() == 1:
                h1_ok = True
        else:
            # Fallback for scalars or other algebraic numbers
            mp = minpoly(witness, x)
            if Poly(mp, x).degree() == 1:
                h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: A is not a scalar multiple of the n \times n identity matrix
    neg_q_ok = False
    try:
        # To be a scalar multiple of the n x n identity matrix, it must be a square matrix.
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix and witness.rows == witness.cols:
            n = witness.rows
            if n == 0:
                is_scalar_mult = True
            else:
                c = witness[0, 0]
                is_scalar_mult = (witness == c * eye(n))
        else:
            # If it's not a square matrix (e.g. a scalar), it cannot be a scalar multiple of the n x n identity matrix
            is_scalar_mult = False
        
        neg_q_ok = not is_scalar_mult
    except Exception:
        # If evaluation fails, we default to False
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The minimal polynomial of A has a degree of exactly 1",
    "¬Q: A is not a scalar multiple of the n x n identity matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1