import sympy as sp
from sympy import eye, zeros, Matrix
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "H_2: \\lambda is an eigenvalue of A",
    "¬Q: The formula for the number of Jordan blocks of size exactly k x k fails"
]

def conditions(witness) -> list[bool]:
    try:
        # The witness can be either (A, lam) or (A, lam, k).
        # If k is not provided, we test k = 0, which is the standard counterexample
        # for the missing "k >= 1" hypothesis.
        if isinstance(witness, tuple):
            if len(witness) == 3:
                A, lam, k = witness
            elif len(witness) == 2:
                A, lam = witness
                k = 0
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: A is an n x n matrix
    try:
        h1 = hasattr(A, 'is_square') and A.is_square
    except Exception:
        h1 = False
        
    # H_2: \lambda is an eigenvalue of A
    try:
        if h1:
            n = A.shape[0]
            I = eye(n)
            # A scalar lambda is an eigenvalue iff A - lambda*I is singular
            h2 = (A - lam * I).rank() < n
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails at the witness
    try:
        if not h1:
            neg_q = False
        else:
            n = A.shape[0]
            I = eye(n)
            N = A - lam * I
            
            # LHS: actual number of Jordan blocks of size exactly k x k
            try:
                if not isinstance(k, (int, sp.Integer)) or k <= 0:
                    lhs = 0
                else:
                    def safe_nullity(m):
                        if m <= 0: 
                            return 0
                        return n - (N**m).rank()
                    lhs = 2 * safe_nullity(k) - safe_nullity(k-1) - safe_nullity(k+1)
            except Exception:
                lhs = 0
                
            # RHS: evaluate the formula exactly as written in the conjecture
            try:
                def exact_nullity(m):
                    # For m < 0, if N is singular (which it is, since lam is an eigenvalue),
                    # N**m will correctly raise an exception, meaning the formula is undefined.
                    return n - (N**m).rank()
                
                rhs = 2 * exact_nullity(k) - exact_nullity(k-1) - exact_nullity(k+1)
                conclusion_holds = (lhs == rhs)
            except Exception:
                # If evaluating the RHS raises an exception (e.g., negative power of a singular matrix),
                # the formula is undefined and thus the equality fails.
                conclusion_holds = False
                
            neg_q = not conclusion_holds
    except Exception:
        # If we cannot even evaluate the conditions, we fail safely
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]