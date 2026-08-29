import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Convert witness to a SymPy Matrix if it isn't already
        A = Matrix(witness)
        # A matrix can only be similar to another matrix (and have a Jordan canonical form)
        # if it is a square matrix. Every square complex matrix is similar to a complex 
        # symmetric matrix. Thus, the conclusion fails iff the matrix is not square.
        neg_q = not A.is_square
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A is not similar to a complex symmetric matrix (e.g., A is not a square matrix)"
]

N_HYP = 0
NEG_Q_INDEX = 0