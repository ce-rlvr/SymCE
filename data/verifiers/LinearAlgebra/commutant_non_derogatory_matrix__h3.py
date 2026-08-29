import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (A, B) of two n x n sympy matrices.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an n x n matrix over a field F (and B is a matrix of the same size)
    try:
        h1 = (isinstance(A, MatrixBase) and 
              isinstance(B, MatrixBase) and 
              A.is_square and B.is_square and 
              A.shape == B.shape)
    except Exception:
        h1 = False

    # H_2: The minimal polynomial of A is equal to the characteristic polynomial of A
    # This is true iff the degree of the minimal polynomial is n, which is equivalent
    # to the matrices I, A, A^2, ..., A^{n-1} being linearly independent.
    try:
        if h1:
            n = A.shape[0]
            if n == 0:
                h2 = True
            else:
                vecs = [list(A**k) for k in range(n)]
                h2 = (Matrix(vecs).rank() == n)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: B cannot be expressed as a polynomial in A with coefficients in F
    # This is true iff B is not in the linear span of I, A, A^2, ..., A^{n-1}.
    try:
        if h1:
            n = A.shape[0]
            if n == 0:
                neg_q = False
            else:
                vecs = [list(A**k) for k in range(n)]
                rank_A = Matrix(vecs).rank()
                
                vecs_B = vecs + [list(B)]
                rank_B = Matrix(vecs_B).rank()
                
                neg_q = (rank_B > rank_A)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F (and B is a matrix of the same size)",
    "H_2: The minimal polynomial of A is equal to the characteristic polynomial of A",
    "¬Q: B cannot be expressed as a polynomial in A with coefficients in F"
]

N_HYP = 2
NEG_Q_INDEX = 2