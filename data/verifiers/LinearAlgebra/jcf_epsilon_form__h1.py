import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should provide a matrix A and a real number epsilon > 0.
    """
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            epsilon = witness.get('epsilon')
        elif isinstance(witness, tuple) and len(witness) == 2:
            is_mat0 = hasattr(witness[0], 'rows') or isinstance(witness[0], list)
            is_mat1 = hasattr(witness[1], 'rows') or isinstance(witness[1], list)
            
            if is_mat0 and not is_mat1:
                A, epsilon = witness
            elif is_mat1 and not is_mat0:
                epsilon, A = witness
            else:
                A, epsilon = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: epsilon > 0 is a real number
    try:
        if hasattr(epsilon, 'is_positive') and epsilon.is_positive:
            h1 = True
        else:
            h1 = bool(epsilon > 0)
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails.
    # The conclusion states there exists an invertible matrix S such that S^{-1}AS is an upper bidiagonal matrix.
    # This is true for all square matrices over C (Epsilon-Jordan Canonical Form).
    # It fails if A is not a square matrix (so S^{-1}AS is undefined or dimensions don't match).
    try:
        if not hasattr(A, 'rows') or not hasattr(A, 'cols'):
            A_mat = Matrix(A)
        else:
            A_mat = A
            
        if A_mat.rows != A_mat.cols:
            q = False
        else:
            q = True
    except Exception:
        # If A cannot even be interpreted as a matrix, the conclusion fails.
        q = False

    return [h1, not q]

CONDITION_LABELS = [
    "H_1: epsilon > 0 is a real number",
    "¬Q: There does not exist an invertible matrix S such that S^{-1}AS is an upper bidiagonal matrix with eigenvalues on the diagonal and 0 or epsilon on the superdiagonal"
]

N_HYP = 1
NEG_Q_INDEX = 1