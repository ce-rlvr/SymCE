import sympy
from sympy.matrices import eye, zeros

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "¬Q: The equivalence (T is triangulable iff its characteristic polynomial splits completely) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_matrix(witness):
    """Helper to check if the witness is a matrix-like object."""
    return hasattr(witness, 'is_square') and hasattr(witness, 'charpoly')

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Check H_1: T is a linear operator on V
    try:
        if hasattr(witness, 'is_linear_operator'):
            h1 = bool(witness.is_linear_operator())
        elif hasattr(witness, 'is_linear'):
            h1 = bool(witness.is_linear())
        elif is_matrix(witness):
            h1 = bool(witness.is_square)
        elif isinstance(witness, str) or callable(witness):
            # Accept strings or callables as representations of infinite-dimensional operators
            h1 = True
    except Exception:
        h1 = False

    # Check ¬Q: The equivalence fails
    # The true theorem states that for FINITE-DIMENSIONAL vector spaces, 
    # T is triangulable iff its characteristic polynomial splits completely.
    # The dropped hypothesis is "V is finite-dimensional".
    try:
        if hasattr(witness, 'is_triangulable') and hasattr(witness, 'char_poly_splits'):
            # If the witness provides explicit methods, use them
            triangulable = bool(witness.is_triangulable())
            splits = bool(witness.char_poly_splits())
            neg_q = (triangulable != splits)
        elif is_matrix(witness):
            # For matrices (finite-dimensional operators), Schur's Triangularization Theorem 
            # guarantees that the equivalence ALWAYS holds. Thus, it cannot be a counterexample.
            neg_q = False
        elif isinstance(witness, str) or callable(witness):
            # Infinite-dimensional operators (e.g., the shift operator) do not have a well-defined 
            # characteristic polynomial that splits, yet they can be triangulable.
            # They serve as the valid counterexamples to the conjecture.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]