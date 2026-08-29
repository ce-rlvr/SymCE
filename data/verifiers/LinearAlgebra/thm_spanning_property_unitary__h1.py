import sympy
from sympy.matrices import MatrixBase, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        # The conclusion states that A can be written as a linear combination of n x n unitary matrices.
        # This implies A must be an n x n (square) matrix.
        # Any square matrix over the complex numbers can be written as a linear combination of 4 unitary matrices.
        # Therefore, the conclusion fails if and only if the witness is not a square matrix.
        if not isinstance(witness, MatrixBase):
            neg_q = True
        elif witness.rows != witness.cols:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A is not a square matrix (cannot be a linear combination of n x n matrices)"
]

N_HYP = 0
NEG_Q_INDEX = 0