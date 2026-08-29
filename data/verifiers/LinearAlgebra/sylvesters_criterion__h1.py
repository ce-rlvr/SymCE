import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not hasattr(witness, "rows") or not hasattr(witness, "cols"):
            return [False]
        if witness.rows != witness.cols:
            return [False]
        
        n = witness.rows
        if n == 0:
            return [False]
            
        minors_positive = True
        for k in range(1, n + 1):
            det_val = witness[:k, :k].det()
            if not (det_val > 0):
                minors_positive = False
                break
                
        is_hermitian = (witness == witness.H)
        
        # Strict definition of positive definite: must be Hermitian and have positive minors
        strict_pd = is_hermitian and minors_positive
        
        # Generalized definition of positive definite: Hermitian part must be positive definite
        sym_part = (witness + witness.H) / 2
        gen_pd = True
        for k in range(1, n + 1):
            det_val = sym_part[:k, :k].det()
            if not (det_val > 0):
                gen_pd = False
                break
                
        # The equivalence fails if it fails under EITHER common definition of positive definite
        neg_q = bool((strict_pd != minors_positive) or (gen_pd != minors_positive))
        
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A is positive definite iff all leading principal minors are strictly positive (equivalence fails)"
]

N_HYP = 0
NEG_Q_INDEX = 0