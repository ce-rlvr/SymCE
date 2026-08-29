import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is a square matrix over a field
    try:
        h1 = bool(getattr(witness, 'is_Matrix', False) and 
                  len(witness.shape) == 2 and 
                  witness.shape[0] == witness.shape[1] and 
                  witness.shape[0] > 0)
    except Exception:
        h1 = False

    # H_2: A is not the zero matrix
    try:
        if h1:
            n = witness.shape[0]
            h2 = bool(witness != zeros(n, n))
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: A is not the identity matrix I_n
    try:
        if h1:
            n = witness.shape[0]
            h3 = bool(witness != eye(n))
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The minimal polynomial of A is not x^2 - x
    try:
        if h1:
            n = witness.shape[0]
            # Under H2 and H3, the minimal polynomial is x^2 - x if and only if A^2 - A = 0.
            # Therefore, the minimal polynomial is NOT x^2 - x if and only if A^2 - A != 0.
            neg_q = bool((witness**2 - witness) != zeros(n, n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix over a field",
    "H_2: A is not the zero matrix",
    "H_3: A is not the identity matrix I_n",
    "¬Q: The minimal polynomial of A is not x^2 - x"
]

N_HYP = 3
NEG_Q_INDEX = 3