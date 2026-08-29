import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A = witness
        if not isinstance(A, Matrix):
            return [False, False]
        
        if A.shape[0] != A.shape[1]:
            return [False, False]
            
        n = A.shape[0]
        I = eye(n)
        evs = A.eigenvals()
        
        # H_1: For every eigenvalue lambda of A, the null space of (A - lambda I) 
        # is equal to the null space of (A - lambda I)^2.
        # By the Rank-Nullity Theorem, since nullspace(M) is a subspace of nullspace(M^2),
        # they are equal if and only if their ranks are equal.
        h1_ok = True
        for lam in evs.keys():
            M = A - lam * I
            if M.rank() != (M**2).rank():
                h1_ok = False
                break
                
        # Conclusion: A is diagonalizable over F.
        # We assume F is the field of real numbers (or a subfield like the rationals).
        # A is diagonalizable over R iff it is diagonalizable over C and all its eigenvalues are real.
        # If it has non-real eigenvalues, it is not diagonalizable over R (nor over Q).
        is_diag_F = A.is_diagonalizable() and all(lam.is_real == True for lam in evs.keys())
        
        # neg_Q is True when the conclusion FAILS (i.e., A is NOT diagonalizable over F)
        neg_q = not is_diag_F
        
        return [h1_ok, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: For every eigenvalue lambda of A, the null space of (A - lambda I) is equal to the null space of (A - lambda I)^2",
    "¬Q: A is not diagonalizable over F"
]

N_HYP = 1
NEG_Q_INDEX = 1