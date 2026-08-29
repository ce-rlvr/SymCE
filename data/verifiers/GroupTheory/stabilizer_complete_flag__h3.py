import sympy
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
    try:
        if isinstance(witness, (list, tuple)):
            M = Matrix(witness)
        else:
            M = witness
        # H_1: The witness represents a complete flag in an n-dimensional vector space.
        # We represent the flag by an invertible n x n matrix whose columns form a basis.
        h1 = isinstance(M, Matrix) and M.is_square and M.shape[0] >= 1
    except Exception:
        h1 = False

    try:
        # H_2: G = GL(V) acts naturally on the set of complete flags of V.
        # This requires the matrix to be invertible so it forms a valid basis/flag.
        h2 = bool(h1 and M.det() != 0)
    except Exception:
        h2 = False

    try:
        # ¬Q: The stabilizer of the flag in G is NOT the subgroup of upper-triangular invertible matrices.
        # The stabilizer of a flag is the subgroup of upper-triangular matrices if and only if
        # the flag is the standard flag, which means its basis matrix M is upper-triangular.
        neg_q = bool(h2 and not M.is_upper)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is an n-dimensional vector space over a field F with a chosen basis e_1, ..., e_n",
    "H_2: G = GL(V) acts naturally on the set of complete flags of V",
    "¬Q: The stabilizer of F in G is not the subgroup of upper-triangular invertible matrices"
]

N_HYP = 2
NEG_Q_INDEX = 2