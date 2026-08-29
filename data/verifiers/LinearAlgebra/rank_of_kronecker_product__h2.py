import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.matrices import MatrixBase, kronecker_product
from sympy.abc import x, y, z

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (A, B) or a dictionary {'A': A, 'B': B}.
    """
    try:
        if isinstance(witness, dict):
            A = witness['A']
            B = witness['B']
        else:
            A, B = witness
    except Exception:
        return [False, False]

    # H_1: A is an m × n matrix over a field F
    try:
        h1 = isinstance(A, MatrixBase)
    except Exception:
        h1 = False

    # ¬Q: rank(A ⊗ B) != rank(A) * rank(B)
    try:
        kron_AB = kronecker_product(A, B)
        rank_kron = kron_AB.rank()
        rank_A = A.rank()
        rank_B = B.rank()
        neg_q = bool(rank_kron != rank_A * rank_B)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m × n matrix over a field F",
    "¬Q: rank(A ⊗ B) != rank(A) * rank(B)"
]

N_HYP = 1
NEG_Q_INDEX = 1