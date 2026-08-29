import sympy as sp
from sympy import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional real or complex vector space",
    "H_2: P is a projection operator on V",
    "¬Q: The matrix exponential e^P is not equal to I + (e - 1)P"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Try to convert the witness to a sympy Matrix if it isn't one already
        if not isinstance(witness, sp.MatrixBase):
            try:
                P = sp.Matrix(witness)
            except Exception:
                return [False, False, False]
        else:
            P = witness
            
        # H_1: V is a finite-dimensional vector space (witness must be a square matrix)
        if not P.is_square:
            return [False, False, False]
        h1 = True
        
        # H_2: P is a projection operator on V (P^2 = P)
        try:
            P_sq = P * P
            h2 = bool(P_sq.equals(P))
        except Exception:
            h2 = False
            
        # ¬Q: The matrix exponential e^P is not equal to I + (e - 1)P
        try:
            I = sp.eye(P.shape[0])
            e = sp.E
            
            # Compute the matrix exponential e^P
            e_P = P.exp()
            
            # Compute the expected result I + (e - 1)P
            expected = I + (e - 1) * P
            
            # Check for equality
            is_equal = e_P.equals(expected)
            if is_equal is None:
                # Fallback to simplify if equals() cannot decide
                diff = sp.simplify(e_P - expected)
                is_equal = bool(diff == sp.zeros(*P.shape))
            else:
                is_equal = bool(is_equal)
                
            neg_q = not is_equal
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]