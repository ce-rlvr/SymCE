import sympy as sp
from sympy.matrices import MatrixBase
from sympy import Matrix, eye, zeros

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The true theorem requires both A and B to be n x n matrices.
    The dropped hypothesis is that A is an n x n matrix.
    """
    try:
        A, B = witness
    except Exception:
        return [False, False]
    
    # H_1: B is an n x n complex matrix
    try:
        h1 = isinstance(B, MatrixBase) and B.rows == B.cols
    except Exception:
        h1 = False
        
    # Conclusion: The minimum singular value of A+B satisfies \sigma_{\min}(A+B) \ge \sigma_{\min}(A) - \sigma_{\max}(B)
    # The inequality is unconditionally true for any matrices A and B of the same size.
    # The conclusion fails (neg_Q is True) if A is not a matrix of the same size, making A+B undefined or ill-typed.
    try:
        C = A + B
    except Exception:
        # If A+B is undefined (e.g., shape mismatch), the conclusion fails.
        return [h1, True]
        
    try:
        # If A is not a matrix (e.g., a scalar), the singular value conclusion is ill-typed and fails.
        if not isinstance(A, MatrixBase):
            return [h1, True]
            
        sv_C = C.singular_values()
        sv_A = A.singular_values()
        sv_B = B.singular_values()
        
        min_sv_C = min([float(abs(s.evalf())) for s in sv_C]) if sv_C else 0.0
        min_sv_A = min([float(abs(s.evalf())) for s in sv_A]) if sv_A else 0.0
        max_sv_B = max([float(abs(s.evalf())) for s in sv_B]) if sv_B else 0.0
        
        # We use a small tolerance to avoid floating point inaccuracies making a true statement false.
        conclusion = min_sv_C >= min_sv_A - max_sv_B - 1e-9
        neg_q = not conclusion
    except Exception:
        # If singular_values() or float conversion fails, it's likely an invalid symbolic witness.
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: B is an n x n complex matrix",
    "¬Q: sigma_min(A+B) < sigma_min(A) - sigma_max(B) or A+B is undefined"
]

N_HYP = 1
NEG_Q_INDEX = 1