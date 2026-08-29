import sympy
from sympy import MatrixBase, eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # H_1: A is an n x n matrix
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            eigenvalues = witness.eigenvals()
            
            # The minimal polynomial of A equals its characteristic polynomial
            # if and only if A is non-derogatory.
            # A matrix is non-derogatory iff the geometric multiplicity of 
            # every eigenvalue is exactly 1.
            # We want neg_q to be True when they are NOT equal (i.e., A is derogatory).
            is_derogatory = False
            for val in eigenvalues.keys():
                # Geometric multiplicity = n - rank(A - lambda * I)
                geom_mult = n - (witness - val * eye(n)).rank()
                if geom_mult > 1:
                    is_derogatory = True
                    break
            
            neg_q = is_derogatory
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The minimal polynomial of A is not equal to the characteristic polynomial of A"
]

N_HYP = 1
NEG_Q_INDEX = 1