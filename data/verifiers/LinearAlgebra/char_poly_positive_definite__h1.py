import sympy as sp
from sympy.matrices import eye, zeros

# Top-level setup for standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Witness must be a square matrix
        if not isinstance(witness, sp.MatrixBase):
            return [False, False]
        if not witness.is_square:
            return [False, False]
        if witness.rows < 1:
            return [False, False]
            
        # H_1: A is positive definite
        # In the context of this false conjecture (where the "symmetric" hypothesis was dropped),
        # positive definite is evaluated via Sylvester's criterion (leading principal minors > 0).
        h1 = True
        for i in range(1, witness.rows + 1):
            minor_det = witness[:i, :i].det()
            if bool(minor_det <= 0):
                h1 = False
                break
                
        # Conclusion: The coefficients of p(t) strictly alternate in sign
        # p(t) = det(tI - A) = t^n + c_{n-1}t^{n-1} + ... + c_0
        t = sp.Symbol('t')
        p = witness.charpoly(t)
        coeffs = p.all_coeffs()  # Returns [c_n, c_{n-1}, ..., c_0]
        
        alternates = True
        for i, c in enumerate(coeffs):
            # coeffs[i] corresponds to c_{n-i}. We need (-1)^{n - (n-i)} c_{n-i} > 0 => (-1)^i c_{n-i} > 0
            sign = (-1)**i
            if bool(sign * c <= 0):
                alternates = False
                break
                
        neg_q = not alternates
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: A is positive definite (leading principal minors > 0)",
    "¬Q: The coefficients of p(t) do not strictly alternate in sign"
]

N_HYP = 1
NEG_Q_INDEX = 1