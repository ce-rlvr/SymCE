import sympy as sp
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
    Given a witness (H, k), checks if it is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that 1 <= k <= n.
    """
    try:
        H, k = witness
    except Exception:
        return [False, False]
        
    # H_1: H is an n x n Hermitian matrix
    try:
        if not isinstance(H, sp.MatrixBase):
            H = sp.Matrix(H)
        n = H.shape[0]
        if H.shape[0] != H.shape[1]:
            h1_ok = False
        else:
            if H == H.H:
                h1_ok = True
            elif H.is_hermitian:
                h1_ok = True
            else:
                h1_ok = False
    except Exception:
        h1_ok = False
        
    # neg_Q: The conclusion FAILS at the witness
    # The conclusion mathematically holds if and only if k is an integer and 1 <= k <= n.
    # If k is out of bounds or not an integer, the maximum over the Stiefel manifold 
    # is undefined/empty, or the sum of k largest eigenvalues is undefined, so they cannot be equal.
    try:
        if float(k) != int(k):
            neg_q_ok = True
        else:
            k_val = int(k)
            if k_val < 1 or k_val > n:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is an n x n Hermitian matrix",
    "¬Q: The sum of the k largest eigenvalues of H is not equal to max { Tr(Q^* H Q) : Q in C^{n x k}, Q^* Q = I_k }"
]

N_HYP = 1
NEG_Q_INDEX = 1