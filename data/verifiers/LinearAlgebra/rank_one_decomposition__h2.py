import sympy
from sympy import Matrix, MatrixBase, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an m x n matrix over a field F and r is an integer
    # Since r is unbound in the remaining hypotheses, the witness must provide it.
    # We expect witness to be a tuple: (A, r)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A_raw, r = witness
            A = Matrix(A_raw)
            h1_ok = isinstance(r, (int, sympy.Integer))
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: The conclusion fails.
    # Conclusion: A can be expressed as the sum of exactly r rank-one matrices, 
    # and cannot be expressed as the sum of fewer than r rank-one matrices.
    # This is the definition of the matrix rank, so the conclusion is equivalent to rank(A) == r.
    # The negated conclusion is rank(A) != r.
    try:
        if h1_ok:
            A_raw, r = witness
            A = Matrix(A_raw)
            neg_q_ok = bool(A.rank() != r)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a matrix and r is an integer",
    "¬Q: rank(A) != r"
]

N_HYP = 1
NEG_Q_INDEX = 1