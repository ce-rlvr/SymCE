import sympy
from sympy import eye, zeros, Matrix, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    """Helper function to robustly check if a SymPy matrix is zero."""
    try:
        if getattr(M, 'is_zero_matrix', False):
            return True
    except Exception:
        pass
    try:
        for i in range(M.rows):
            for j in range(M.cols):
                if sympy.simplify(M[i, j]) != 0:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    # H_1: A is a normal matrix
    try:
        # A matrix is normal if it commutes with its conjugate transpose
        diff_normal = witness * witness.H - witness.H * witness
        h1 = is_zero_mat(diff_normal)
    except Exception:
        h1 = False

    # H_2: Every eigenvalue of A has an absolute value equal to 1
    try:
        eigenvals = witness.eigenvals()
        h2 = True
        # witness.eigenvals() returns a dict of {eigenvalue: multiplicity}
        # Iterating over it yields the eigenvalues.
        for eig in eigenvals:
            if sympy.simplify(abs(eig) - 1) != 0:
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: A is NOT a unitary matrix
    try:
        # A matrix is unitary if A * A.H == I
        I = eye(witness.rows)
        diff_unitary = witness * witness.H - I
        is_unitary = is_zero_mat(diff_unitary)
        neg_q = not is_unitary
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a normal matrix",
    "H_2: Every eigenvalue of A has an absolute value equal to 1",
    "¬Q: A is not a unitary matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2