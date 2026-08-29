import sympy
from sympy import Matrix, eye, zeros, I
from sympy.abc import x, y, z

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is an invertible matrix
    try:
        h1 = bool(witness.is_square and witness.det() != 0)
    except Exception:
        h1 = False

    # ¬Q: There does NOT exist a unique real orthogonal matrix Q and a unique 
    # real symmetric positive definite matrix P such that A = QP.
    # If A is real and invertible, such Q and P always exist and are unique.
    # If A is not real, A cannot be the product of two real matrices, so no such Q and P exist.
    try:
        is_real = True
        for elem in witness:
            if hasattr(elem, 'is_real') and elem.is_real is False:
                is_real = False
                break
            if hasattr(elem, 'has') and elem.has(sympy.I):
                is_real = False
                break
            if isinstance(elem, complex) and elem.imag != 0:
                is_real = False
                break
        neg_q = not is_real
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an invertible matrix",
    "¬Q: There does not exist a unique real orthogonal Q and real symmetric positive definite P such that A = QP"
]

N_HYP = 1
NEG_Q_INDEX = 1