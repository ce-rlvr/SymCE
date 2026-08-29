import sympy as sp
from sympy.matrices import MatrixBase, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            P = witness.get('P')
            b = witness.get('b')
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            P = witness[0]
            b = witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: P is an idempotent matrix
    try:
        h1 = isinstance(P, MatrixBase) and P.is_square and (P**2 == P)
    except Exception:
        h1 = False

    # ¬Q: The linear system Px = b has a solution if and only if Pb = b
    try:
        if not isinstance(b, MatrixBase):
            b_mat = sp.Matrix(b)
        else:
            b_mat = b

        # Check if Px = b has a solution (rank of coefficient matrix equals rank of augmented matrix)
        aug = P.row_join(b_mat)
        has_solution = (P.rank() == aug.rank())

        # Check if Pb = b
        pb_equals_b = (P * b_mat == b_mat)

        # The conclusion fails if the biconditional is false
        neg_q = (has_solution != pb_equals_b)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is an idempotent matrix",
    "¬Q: The equivalence (Px = b has a solution iff Pb = b) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1