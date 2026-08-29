import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        Q, A = witness
    except Exception:
        return [False, False]

    # H_1: A is an m x n real matrix
    try:
        h1 = getattr(A, 'is_Matrix', False) and all(e.is_real for e in A)
    except Exception:
        h1 = False

    # ¬Q: The Frobenius norm of QA is not equal to the Frobenius norm of A
    try:
        neg_q = False
        if getattr(Q, 'is_Matrix', False) and getattr(A, 'is_Matrix', False):
            if Q.cols == A.rows:
                QA = Q * A
                norm_QA = QA.norm()
                norm_A = A.norm()
                if norm_QA != norm_A:
                    diff = sympy.simplify(norm_QA - norm_A)
                    if diff != 0:
                        neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an m x n real matrix",
    "¬Q: The Frobenius norm of QA is not equal to the Frobenius norm of A"
]

N_HYP = 1
NEG_Q_INDEX = 1