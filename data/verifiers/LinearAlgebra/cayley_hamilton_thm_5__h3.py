import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    A = None
    c_0 = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, c_0 = witness
        elif isinstance(witness, dict):
            A = witness.get('A')
            c_0 = witness.get('c_0')
        else:
            A = witness
            # If c_0 is not provided, we assume it is a free variable 
            # and set it to 1 to help singular matrices fail the conclusion.
            c_0 = 1
    except Exception:
        return [False, False, False]

    # H_1: F is a field.
    # We verify that A is a SymPy matrix, which implicitly operates over the field of fractions of its entries.
    try:
        h1 = isinstance(A, sp.MatrixBase)
    except Exception:
        h1 = False

    # H_2: A is an n x n matrix with entries in F.
    try:
        h2 = bool(A.is_square)
    except Exception:
        h2 = False

    # ¬Q: The conclusion "A is an invertible matrix if and only if c_0 != 0" fails.
    try:
        is_invertible = bool(A.det() != 0)
        c0_neq_0 = bool(c_0 != 0)
        neg_q = not (is_invertible == c0_neq_0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is an n x n matrix with entries in F",
    "¬Q: A is not (invertible iff c_0 != 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2