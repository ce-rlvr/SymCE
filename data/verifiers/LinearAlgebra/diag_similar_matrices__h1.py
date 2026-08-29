import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _extract_AB(witness):
    """Helper to unpack the witness into matrices A and B."""
    if isinstance(witness, tuple) and len(witness) == 2:
        return witness[0], witness[1]
    elif isinstance(witness, dict) and 'A' in witness and 'B' in witness:
        return witness['A'], witness['B']
    else:
        # Fallback: if only one matrix is provided, assume A = B
        return witness, witness

def conditions(witness) -> list[bool]:
    try:
        A, B = _extract_AB(witness)
        h1 = bool(hasattr(B, 'is_square') and B.is_square and 
                  hasattr(A, 'is_square') and A.is_square and 
                  A.shape == B.shape)
    except Exception:
        h1 = False

    try:
        A, B = _extract_AB(witness)
        if hasattr(B, 'is_similar'):
            h2 = bool(B.is_similar(A))
        else:
            h2 = bool(A.jordan_form()[1] == B.jordan_form()[1])
    except Exception:
        h2 = False

    try:
        A, B = _extract_AB(witness)
        neg_q = not bool(B.is_diagonalizable())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is an n x n matrix over the field F",
    "H_2: B is similar to A",
    "¬Q: B is not diagonalizable over the field F"
]

N_HYP = 2
NEG_Q_INDEX = 2