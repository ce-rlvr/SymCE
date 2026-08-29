import sympy
from sympy import MatrixBase, eye, zeros

# Top-level setup for linear algebra witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is an m x n complex matrix
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    # ¬Q: Every singular value of A is either exactly 0 or exactly 1 (Negated: at least one is not 0 and not 1)
    try:
        if not h1:
            neg_q = False
        else:
            # The singular values of A are the square roots of the eigenvalues of A^* A.
            # Since A^* A is Hermitian (and thus diagonalizable), its eigenvalues are all exactly 0 or 1
            # if and only if it is idempotent, i.e., (A^* A)^2 = A^* A.
            M = witness.H * witness
            diff = M * M - M
            
            is_idempotent = True
            for val in diff:
                v = sympy.simplify(val)
                if v != 0 and v.is_zero is not True:
                    is_idempotent = False
                    break
            
            # If it is NOT idempotent, then it has an eigenvalue that is not 0 or 1,
            # which means A has a singular value that is not 0 or 1.
            neg_q = not is_idempotent
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: A has at least one singular value that is neither exactly 0 nor exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1