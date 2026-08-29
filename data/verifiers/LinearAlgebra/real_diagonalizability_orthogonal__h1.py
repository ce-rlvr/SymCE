import sympy
from sympy import Matrix, I, sqrt, simplify, im, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_real_val(val):
    """Check if a SymPy expression or number is strictly real."""
    if hasattr(val, 'is_real') and val.is_real is not None:
        return val.is_real
    try:
        c = complex(val)
        return c.imag == 0
    except Exception:
        pass
    try:
        return simplify(im(val)) == 0
    except Exception:
        return False

def is_diagonalizable_over_R(Q):
    """
    A matrix is diagonalizable over the real numbers if:
    1. It is a real matrix.
    2. It is diagonalizable over C.
    3. All its eigenvalues are real.
    """
    try:
        if not all(is_real_val(val) for val in Q):
            return False
        if not Q.is_diagonalizable():
            return False
        for ev in Q.eigenvals():
            if not is_real_val(ev):
                return False
        return True
    except Exception:
        return False

def is_symmetric(Q):
    try:
        if not getattr(Q, 'is_square', False):
            return False
        diff = Q - Q.T
        return all(simplify(val) == 0 for val in diff)
    except Exception:
        return False

def is_orthogonal(Q):
    try:
        if not getattr(Q, 'is_square', False):
            return False
        diff = Q.T * Q - eye(Q.shape[0])
        return all(simplify(val) == 0 for val in diff)
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = is_orthogonal(witness)
    except Exception:
        h1 = False
        
    try:
        diag_R = is_diagonalizable_over_R(witness)
        sym = is_symmetric(witness)
        concl = (diag_R == sym)
        neg_q = not concl
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "¬Q: The equivalence 'Q is diagonalizable over the real numbers iff Q is a symmetric matrix' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1