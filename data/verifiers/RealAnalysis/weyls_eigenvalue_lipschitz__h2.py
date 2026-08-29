import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup for potential witness expressions
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that the k-th largest eigenvalue is 1-Lipschitz continuous 
    on the vector space of n x n real symmetric matrices. 
    Without specifying the Frobenius or operator norm, the standard norm on the 
    vector space S_n (isomorphic to R^{n(n+1)/2}) is the Euclidean norm on its 
    independent coordinates. Under this norm, the map is NOT 1-Lipschitz.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                A_raw, B_raw, k = witness
                k_provided = True
            elif len(witness) == 2:
                A_raw, B_raw = witness
                k_provided = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        A = Matrix(A_raw)
        B = Matrix(B_raw)
    except Exception:
        return [False, False, False]

    # H_1: S_n is the vector space of n x n real symmetric matrices.
    # We verify that the witness matrices A and B belong to S_n.
    try:
        n = A.shape[0]
        h1 = (A.shape == (n, n) and B.shape == (n, n) and 
              A.is_symmetric() and B.is_symmetric() and
              all(A[i,j].is_real for i in range(n) for j in range(n)) and
              all(B[i,j].is_real for i in range(n) for j in range(n)))
    except Exception:
        h1 = False

    # H_2: \lambda_k(A) denotes the k-th largest eigenvalue of a matrix A in S_n, where 1 <= k <= n.
    try:
        if h1:
            if k_provided:
                h2 = (isinstance(k, int) and 1 <= k <= n)
                k_list = [k]
            else:
                h2 = True
                k_list = list(range(1, n + 1))
        else:
            h2 = False
            k_list = []
    except Exception:
        h2 = False
        k_list = []

    # ¬Q: The function mapping A to \lambda_k(A) is NOT 1-Lipschitz continuous on S_n.
    # We check if |\lambda_k(A) - \lambda_k(B)| > ||A - B||_E
    # where ||.||_E is the standard Euclidean norm on the independent coordinates of S_n.
    try:
        neg_q = False
        if h1 and h2:
            evals_A = A.eigenvals(multiple=True)
            evals_B = B.eigenvals(multiple=True)
            
            # Evaluate symbolically to floats and sort descending (k-th largest)
            evals_A_float = sorted([float(sympy.re(sympy.N(e))) for e in evals_A], reverse=True)
            evals_B_float = sorted([float(sympy.re(sympy.N(e))) for e in evals_B], reverse=True)
            
            # Compute the Euclidean norm on the independent entries (upper triangular part)
            norm_E_sq = sum(float(sympy.re(sympy.N(A[i,j] - B[i,j])))**2 for i in range(n) for j in range(i, n))
            norm_E = norm_E_sq ** 0.5
            
            for k_val in k_list:
                lam_A = evals_A_float[k_val-1]
                lam_B = evals_B_float[k_val-1]
                diff = abs(lam_A - lam_B)
                
                # If the difference exceeds the norm, it is not 1-Lipschitz
                if diff > norm_E + 1e-9:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are in S_n (n x n real symmetric matrices)",
    "H_2: k is a valid index (1 <= k <= n)",
    "¬Q: The function mapping A to \\lambda_k(A) is not 1-Lipschitz continuous on S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2