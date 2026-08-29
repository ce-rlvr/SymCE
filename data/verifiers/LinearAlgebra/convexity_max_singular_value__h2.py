import sympy as sp
from sympy.matrices import eye, zeros, Matrix
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, B, t = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(getattr(A, 'is_Matrix', False) and getattr(B, 'is_Matrix', False) and A.shape == B.shape)
        # Ensure t is a scalar that can be evaluated to a complex number
        _ = complex(t)
    except Exception:
        h1 = False

    # The second hypothesis is definitional and holds by the definition of sigma1 in our logic
    h2 = True

    try:
        def sigma1(M):
            svals = M.singular_values()
            if not svals:
                return 0.0
            return max([abs(complex(s.evalf())) for s in svals])
            
        lhs_mat = t * A + (1 - t) * B
        lhs_val = sigma1(lhs_mat)
        
        s1_A = sigma1(A)
        s1_B = sigma1(B)
        rhs_val = t * s1_A + (1 - t) * s1_B
        
        rhs_c = complex(rhs_val)
        # If the right-hand side is complex with a non-zero imaginary part, 
        # the standard <= inequality is undefined, meaning the conclusion fails.
        if abs(rhs_c.imag) > 1e-7:
            neg_q = True
        else:
            # The conclusion is LHS <= RHS. It fails if LHS > RHS.
            neg_q = bool(lhs_val > rhs_c.real + 1e-7)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are m x n complex matrices",
    "H_2: sigma_1(.) denotes the maximum singular value of a matrix",
    "¬Q: sigma_1(tA + (1-t)B) > t*sigma_1(A) + (1-t)*sigma_1(B)"
]

N_HYP = 2
NEG_Q_INDEX = 2