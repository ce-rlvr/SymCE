import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims every matrix has a Schur decomposition (A = U T U^*).
    This is true for square matrices over C, but fails for non-square matrices.
    """
    try:
        # Convert lists/tuples to SymPy Matrix if necessary
        if isinstance(witness, (list, tuple)):
            witness = Matrix(witness)
            
        # The conclusion fails if A is not a square matrix, because U T U^* 
        # (with U being a unitary matrix, hence square) is always a square matrix.
        neg_q = not witness.is_square
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A is not a square matrix, so it cannot be decomposed as U T U^*"
]

N_HYP = 0
NEG_Q_INDEX = 0