import sympy
from sympy import MatrixBase, Integer, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (A, k) where A is a matrix and k is an integer.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, k = witness
        else:
            A = witness
            k = None
    except Exception:
        A = witness
        k = None

    # H_1: A is an m x n complex matrix
    try:
        h1 = isinstance(A, MatrixBase)
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails
    try:
        if not h1:
            neg_q = False
        elif k is None:
            # If k is not provided, the witness is incomplete for a theorem parameterized by k.
            neg_q = False
        elif not isinstance(k, (int, Integer)):
            neg_q = True
        else:
            m, n = A.shape
            # The conclusion states an equality for the k-th singular value.
            # If k < 1 or k > min(m, n), the k-th singular value is undefined,
            # or the subspace dimension k is invalid (e.g., k > n),
            # so the equality fails.
            if k < 1 or k > min(m, n):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: The conclusion fails (e.g., k is out of bounds so the equality is undefined or false)"
]

N_HYP = 1
NEG_Q_INDEX = 1