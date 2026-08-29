import sympy
from sympy import Matrix, MatrixBase, zeros, eye
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
        if isinstance(witness, dict):
            A = witness.get('A')
            U = witness.get('U')
            Sigma = witness.get('Sigma')
            V = witness.get('V')
            if A is None or U is None or Sigma is None or V is None:
                return [False, False]
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            A, U, Sigma, V = witness[:4]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(A, MatrixBase)
    except Exception:
        h1 = False

    try:
        if not isinstance(U, MatrixBase):
            U = Matrix(U)
        if not isinstance(Sigma, MatrixBase):
            Sigma = Matrix(Sigma)
        if not isinstance(V, MatrixBase):
            V = Matrix(V)

        r = A.rank()
        sum_mat = zeros(A.rows, A.cols)
        for i in range(r):
            sum_mat += Sigma[i, i] * U[:, i] * V[:, i].H
        
        q = (A == sum_mat)
        neg_q = not q
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over C with rank r",
    "¬Q: A cannot be expressed as the sum of sigma_i u_i v_i^* for i=1..r"
]
N_HYP = 1
NEG_Q_INDEX = 1