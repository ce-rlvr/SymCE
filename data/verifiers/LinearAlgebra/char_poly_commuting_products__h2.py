import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        else:
            A, B = witness
    except Exception:
        return [False, False]

    # H_1: A is an n x n matrix over a field F
    try:
        h1 = hasattr(A, 'is_Matrix') and A.is_Matrix and A.rows == A.cols
    except Exception:
        h1 = False

    # Conclusion: The characteristic polynomial of AB is equal to the characteristic polynomial of BA
    try:
        cp_AB = (A * B).charpoly()
        cp_BA = (B * A).charpoly()
        q_ok = (cp_AB == cp_BA)
    except Exception:
        # If multiplication is undefined or the resulting matrices are not square,
        # they do not have equal characteristic polynomials.
        q_ok = False

    neg_q = not q_ok

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "¬Q: The characteristic polynomial of AB is not equal to the characteristic polynomial of BA (or is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1