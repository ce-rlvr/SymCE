import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n \times n matrix over the real numbers
    try:
        if isinstance(witness, MatrixBase) and witness.is_square:
            h1 = True
            for elem in witness:
                sym_elem = sympy.sympify(elem)
                if not sym_elem.is_real:
                    h1 = False
                    break
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: A is a skew-symmetric matrix, satisfying A^T = -A
    try:
        h2 = bool(witness.transpose() == -witness)
    except Exception:
        h2 = False

    # neg_Q: 0 is NOT a root of the characteristic polynomial of A
    try:
        # 0 is a root of the characteristic polynomial iff det(A) == 0.
        # Thus, 0 is NOT a root iff det(A) != 0.
        neg_q = bool(sympy.simplify(witness.det()) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix over the real numbers",
    "H_2: A is a skew-symmetric matrix (A^T = -A)",
    "¬Q: 0 is not a root of the characteristic polynomial of A"
]

N_HYP = 2
NEG_Q_INDEX = 2