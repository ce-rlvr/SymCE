import sympy
from sympy import eye, zeros
from sympy.matrices import MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The conjecture states that every matrix A has a Singular Value Decomposition (SVD)
    with unitary matrices U, V and a diagonal matrix Sigma with non-negative real entries.
    This is true for all complex matrices. It fails if A is not a complex matrix 
    (e.g., a matrix with symbolic/polynomial entries, or not a matrix at all).
    """
    try:
        # The conclusion fails if the witness is not a matrix
        if not isinstance(witness, MatrixBase):
            neg_q = True
        else:
            neg_q = False
            # The conclusion fails if the matrix has entries that are not complex numbers
            # (e.g., free symbols, polynomials, or elements from other fields)
            for e in witness:
                if not e.is_number or not e.is_complex:
                    neg_q = True
                    break
    except Exception:
        neg_q = True

    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: A does not have a Singular Value Decomposition over the complex numbers"
]

N_HYP = 0
NEG_Q_INDEX = 0