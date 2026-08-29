import sympy
from sympy import eye, zeros, MatrixBase

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
O0 = zeros(0, 0)

def conditions(witness) -> list[bool]:
    try:
        # V is a finite-dimensional vector space over C
        # We represent the vector space and the operator by a matrix.
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    try:
        # T is a linear operator on V
        # Represented by the matrix being square.
        h2 = h1 and witness.is_square
    except Exception:
        h2 = False

    try:
        # V contains a 1-dimensional T-invariant subspace.
        # Over C, every linear operator on a space of dimension >= 1 has an eigenvalue,
        # and therefore a 1-dimensional invariant subspace.
        # The conclusion fails (neg_Q is True) iff the dimension of V is 0.
        if h2:
            neg_q = (witness.shape[0] == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over the field of complex numbers",
    "H_2: T is a linear operator on V",
    "¬Q: V does not contain a 1-dimensional T-invariant subspace"
]

N_HYP = 2
NEG_Q_INDEX = 2