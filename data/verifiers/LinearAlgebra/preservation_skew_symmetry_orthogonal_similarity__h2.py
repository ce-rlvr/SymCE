import sympy as sp
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (A, Q) or a dictionary {'A': A, 'Q': Q}.
    """
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            Q = witness.get('Q')
        else:
            A, Q = witness
    except Exception:
        return [False, False]
        
    # H_1: A is an n x n real skew-symmetric matrix
    try:
        h1 = False
        if isinstance(A, MatrixBase) and isinstance(Q, MatrixBase) and A.is_square:
            # Check if all elements are explicitly real
            if all(e.is_real for e in A):
                # Check if A is skew-symmetric (A = -A^T)
                sym_diff = A + A.T
                if all(sp.simplify(e) == 0 for e in sym_diff):
                    h1 = True
    except Exception:
        h1 = False

    # ¬Q: The matrix Q A Q^T is NOT a skew-symmetric matrix
    try:
        M = Q * A * Q.T
        diff = M + M.T
        # If M is skew-symmetric, diff should be the zero matrix.
        # We want the negated conclusion, so it must NOT be the zero matrix.
        neg_q = any(sp.simplify(e) != 0 for e in diff)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real skew-symmetric matrix",
    "¬Q: The matrix Q A Q^T is not a skew-symmetric matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1