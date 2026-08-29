import sympy
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Ensure the witness is a sympy Matrix
        if not isinstance(witness, sympy.MatrixBase):
            witness = sympy.Matrix(witness)
            
        n = witness.rows
        if witness.cols != n:
            # Non-square matrices cannot be factored into square Givens rotations
            neg_q = True
        else:
            # A product of unitary matrices (diagonal unitary and Givens rotations) is unitary.
            # If U is not unitary, it cannot be factored in this way.
            diff = sympy.simplify(witness * witness.H - eye(n))
            is_unitary = (diff == zeros(n, n))
            neg_q = not is_unitary
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: U cannot be factored into a diagonal unitary matrix and at most n(n-1)/2 Givens rotations (e.g., U is not unitary)"
]

N_HYP = 0
NEG_Q_INDEX = 0