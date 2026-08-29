import sympy as sp

# Top-level setup
# No special named groups or rings are needed for this linear algebra theorem.
# The witness is expected to be a tuple (A, b, x) of sympy Matrices.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (A, b, x).
    """
    try:
        A, b, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: b is a vector in C^n
    try:
        h1 = isinstance(b, sp.MatrixBase) and b.cols == 1 and A.rows == b.rows
    except Exception:
        h1 = False

    # H2: x is the unique solution to the linear system Ax = b
    try:
        if not isinstance(x, sp.MatrixBase) or x.cols != 1 or A.cols != x.rows:
            h2 = False
        else:
            is_solution = (A * x == b)
            # The solution is unique if and only if the nullspace of A is trivial
            is_unique = len(A.nullspace()) == 0
            h2 = is_solution and is_unique
    except Exception:
        h2 = False

    # H3: \sigma_{min}(A) is the smallest singular value of A
    # This is a declarative definition. We return True as long as A is a valid matrix.
    try:
        h3 = isinstance(A, sp.MatrixBase)
    except Exception:
        h3 = False

    # Conclusion: The Euclidean norm of x satisfies ||x||_2 <= ||b||_2 / \sigma_{min}(A)
    # We evaluate the negation of the conclusion (neg_Q).
    try:
        svs = A.singular_values()
        if not svs:
            # If the matrix has no singular values (e.g., a 0x0 empty matrix), 
            # the minimum singular value is undefined, so the conclusion fails.
            neg_q = True
        else:
            sigma_min = min(svs)
            if sigma_min == 0:
                # Division by zero makes the conclusion fail
                neg_q = True
            else:
                norm_x = x.norm()
                norm_b = b.norm()
                # The conclusion holds if norm_x <= norm_b / sigma_min
                holds = bool(norm_x <= norm_b / sigma_min)
                neg_q = not holds
    except Exception:
        # If evaluation fails (e.g., undefined division or norm), the conclusion fails
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: b is a vector in C^n",
    "H_2: x is the unique solution to the linear system Ax = b",
    "H_3: \sigma_{min}(A) is the smallest singular value of A",
    "¬Q: The Euclidean norm of x does NOT satisfy ||x||_2 <= ||b||_2 / \sigma_{min}(A) (e.g. undefined)"
]

N_HYP = 3
NEG_Q_INDEX = 3