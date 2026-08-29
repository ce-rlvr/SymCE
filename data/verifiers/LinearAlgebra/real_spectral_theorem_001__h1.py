import sympy
from sympy import eye, zeros, Matrix
from sympy.matrices import MatrixBase
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, MatrixBase):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = all((e.is_real == True) if hasattr(e, 'is_real') else (sympy.sympify(e).is_real == True) for e in witness)
    except Exception:
        h1 = False

    try:
        h2 = witness.is_square and witness == witness.T
    except Exception:
        h2 = False

    try:
        # The conclusion states: There exists a real orthogonal matrix Q and a real diagonal matrix D 
        # such that A = Q D Q^T.
        # Mathematically, for finite-dimensional matrices, this is exactly equivalent to A being 
        # a real symmetric matrix (by the Real Spectral Theorem).
        q_holds = h1 and h2
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The entries of A are real numbers",
    "H_2: A is a symmetric matrix (A^T = A)",
    "¬Q: There does not exist a real orthogonal matrix Q and a real diagonal matrix D such that A = Q D Q^T"
]

N_HYP = 2
NEG_Q_INDEX = 2