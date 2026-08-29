import sympy
from sympy.matrices import MatrixBase, Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n matrix with real entries
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square and all(e.is_real for e in witness)
    except Exception:
        h1 = False

    # H_2: A is symmetric
    try:
        h2 = isinstance(witness, MatrixBase) and witness.is_symmetric()
    except Exception:
        h2 = False

    # ¬Q: The bilinear form does not satisfy the axioms of an inner product
    # A bilinear form x^T A y is an inner product on R^n iff A is symmetric and positive definite.
    try:
        if isinstance(witness, MatrixBase) and witness.is_square:
            if not witness.is_symmetric():
                neg_q = True
            else:
                # Sylvester's criterion for positive definiteness
                n = witness.rows
                is_pos_def = True
                for i in range(1, n + 1):
                    if witness[:i, :i].det() <= 0:
                        is_pos_def = False
                        break
                neg_q = not is_pos_def
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "H_2: A is symmetric",
    "¬Q: The bilinear form does not satisfy the axioms of an inner product (A is not positive definite)"
]

N_HYP = 2
NEG_Q_INDEX = 2