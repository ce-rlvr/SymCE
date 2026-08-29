import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices.matrixbase import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, sigma = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(A, MatrixBase)
        _ = sigma + 1  # check if sigma is a scalar
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            A_H_A = A.H * A
            eigenvals = A_H_A.eigenvals()
            sigma_sq = sigma**2
            
            is_eigenval = False
            for ev in eigenvals:
                if sympy.simplify(ev - sigma_sq) == 0:
                    is_eigenval = True
                    break
                    
            sigma_sym = sympy.sympify(sigma)
            try:
                s_vals = A.singular_values()
                is_singular_value = False
                for s in s_vals:
                    if sympy.simplify(s - sigma_sym) == 0:
                        is_singular_value = True
                        break
            except Exception:
                # Fallback if singular_values() fails
                is_singular_value = False
                try:
                    if sigma_sym.is_real and sigma_sym >= 0:
                        is_singular_value = is_eigenval
                except Exception:
                    pass
                    
            # The conclusion states: sigma is a singular value iff sigma^2 is an eigenvalue of A^*A
            # We want the conclusion to FAIL, so the truth values must differ.
            neg_q = (is_singular_value != is_eigenval)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: The equivalence between sigma being a singular value of A and sigma^2 being an eigenvalue of A^*A FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1