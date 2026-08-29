import sympy
from sympy.matrices import MatrixBase
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    Checks if the witness is a valid counterexample.
    The witness is expected to be a square sympy Matrix representing a bilinear form B on V = F^n.
    """
    try:
        # H_1: V is a vector space over a field F
        # A square matrix implicitly defines a bilinear form on the vector space F^n.
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        # H_2: R is the radical of B
        # This is true by definition for our matrix representation, 
        # where R is the nullspace (radical) of the bilinear form.
        h2 = h1
    except Exception:
        h2 = False

    try:
        # ¬Q: The induced map on V/R is not a well-defined non-degenerate symmetric bilinear form.
        # The map \bar{B}(u+R, v+R) = B(u, v) is well-defined, non-degenerate, and symmetric 
        # if and only if the original bilinear form B is symmetric.
        # Thus, the conclusion fails (¬Q is True) iff the matrix is NOT symmetric.
        if h1:
            neg_q = not witness.is_symmetric()
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: R is the radical of B",
    "¬Q: The induced map on V/R is not a well-defined non-degenerate symmetric bilinear form"
]

N_HYP = 2
NEG_Q_INDEX = 2