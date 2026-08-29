import sympy
from sympy import eye, zeros

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be the dimension n (an integer) or an n x n matrix.
    """
    # H_1: Let M_n(F) be the vector space of n x n matrices over a field F
    try:
        if hasattr(witness, 'shape'):
            n = witness.shape[0]
            h1 = (n >= 0 and witness.shape[0] == witness.shape[1])
        else:
            n = int(witness)
            h1 = (n >= 0)
    except Exception:
        h1 = False

    # ¬Q: C is NOT a subspace of M_n(F) with dimension 1
    try:
        if hasattr(witness, 'shape'):
            n = witness.shape[0]
        else:
            n = int(witness)
            
        if n < 0:
            neg_q = False
        else:
            # The center of M_n(F) consists of scalar matrices.
            # For n >= 1, the dimension is 1.
            # For n = 0, the dimension is 0.
            dim = 1 if n >= 1 else 0
            neg_q = bool(dim != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M_n(F) is the vector space of n x n matrices over a field F",
    "¬Q: C is not a subspace of M_n(F) with dimension 1"
]

N_HYP = 1
NEG_Q_INDEX = 1