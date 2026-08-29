import sympy
from sympy import Matrix, eye, zeros
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

def kronecker_product(A, B):
    """Computes the Kronecker product of two matrices."""
    m, n = A.shape
    p, q = B.shape
    return Matrix(m * p, n * q, lambda i, j: A[i // p, j // q] * B[i % p, j % q])

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n diagonalizable matrix over a field F
    try:
        if isinstance(witness, tuple):
            A = witness[0]
        else:
            A = witness
            
        if not isinstance(A, Matrix):
            H1 = False
        elif A.shape[0] != A.shape[1]:
            H1 = False
        else:
            H1 = A.is_diagonalizable()
    except Exception:
        H1 = False

    # ¬Q: The linear operator L is NOT diagonalizable
    try:
        L = None
        if isinstance(witness, tuple):
            if len(witness) == 2:
                second = witness[1]
                # If the witness is (A, B), L is the generalized commutator operator L(X) = AX - XB
                if isinstance(second, Matrix) and second.shape == A.shape:
                    B = second
                    n = A.shape[0]
                    I = eye(n)
                    L = kronecker_product(A, I) - kronecker_product(I, B.T)
                # If the witness is (A, L), where L is explicitly given as the operator matrix
                elif isinstance(second, Matrix) and second.shape == (A.shape[0]**2, A.shape[0]**2):
                    L = second
        else:
            # If the witness is just A, L is the standard commutator operator L(X) = AX - XA
            n = A.shape[0]
            I = eye(n)
            L = kronecker_product(A, I) - kronecker_product(I, A.T)
            
        if L is None:
            neg_Q = False
        else:
            neg_Q = not L.is_diagonalizable()
    except Exception:
        neg_Q = False

    return [bool(H1), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: A is an n x n diagonalizable matrix over a field F",
    "¬Q: The linear operator L is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1