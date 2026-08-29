import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is an n-dimensional vector space",
    "¬Q: dim(intersection of ker(f_i)) < n - k"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Extract the list of linear maps (matrices) from the witness
        if isinstance(witness, dict):
            F = witness.get('f', witness.get('F', witness.get('f_i', witness.get('funcs', []))))
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                _, _, F = witness
            elif len(witness) == 2:
                _, F = witness
            else:
                F = witness[-1]
        elif isinstance(witness, list):
            F = witness
        else:
            F = [witness]
            
        # Verify H_1: V is an n-dimensional vector space
        # This means all f_i must be linear maps from the same n-dimensional space
        if F and isinstance(F, list):
            if all(hasattr(M, 'cols') and hasattr(M, 'rows') for M in F):
                n = F[0].cols
                k = len(F)
                if n > 0 and k > 0 and all(M.cols == n for M in F):
                    h1 = True
    except Exception:
        h1 = False

    try:
        if h1:
            # Stack all matrices vertically to find the intersection of their kernels
            stacked = F[0]
            for M in F[1:]:
                stacked = stacked.col_join(M)
            
            # By Rank-Nullity Theorem, dim(ker) = n - rank
            dim_ker = n - stacked.rank()
            
            # Check if the conclusion fails
            neg_q = bool(dim_ker < n - k)
    except Exception:
        neg_q = False

    return [h1, neg_q]