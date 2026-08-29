import sympy
from sympy import Matrix, eye, zeros, MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_psd(M):
    """Check if a matrix is positive semi-definite."""
    if not isinstance(M, MatrixBase):
        return False
    if not M.is_square:
        return False
    
    # Check if Hermitian
    if M != M.H:
        try:
            diff = M - M.H
            if not all(abs(complex(x.evalf())) < 1e-9 for x in diff):
                return False
        except Exception:
            return False
            
    # Check if all eigenvalues are real and non-negative
    try:
        evs = M.eigenvals()
        for ev in evs:
            val = complex(ev.evalf())
            if abs(val.imag) > 1e-7:
                return False
            if val.real < -1e-7:
                return False
    except Exception:
        return False
        
    return True

def conditions(witness):
    """
    Evaluates the remaining hypotheses and the negated conclusion.
    The witness is expected to be a square matrix representing the linear operator T.
    """
    # H_1: V is a finite-dimensional inner product space (witness T is a square matrix)
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # ¬Q: There does not exist a unique positive semi-definite linear operator S such that S^2 = T.
    # A matrix T has a unique positive semi-definite square root if and only if T itself is positive semi-definite.
    # Thus, the conclusion fails (neg_Q is True) iff T is NOT positive semi-definite.
    try:
        neg_q = not is_psd(witness)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space (witness is a square matrix)",
    "¬Q: There does not exist a unique positive semi-definite linear operator S such that S^2 = T"
]

N_HYP = 1
NEG_Q_INDEX = 1