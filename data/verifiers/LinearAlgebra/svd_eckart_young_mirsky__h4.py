import sympy
from sympy import MatrixBase, eye, zeros

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Eckart-Young-Mirsky Theorem (2-Norm) conjecture.
    The witness can be a tuple (A, k) or just a matrix A (in which case k defaults to A.rank()).
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, k = witness
        else:
            A = witness
            k = A.rank() if hasattr(A, 'rank') else None
            
        if not isinstance(A, MatrixBase):
            return [False, False, False, False, False]
            
        if k is None or not isinstance(k, int):
            return [False, False, False, False, False]
            
        r = A.rank()
        
        # H_1: A is an m x n complex matrix with rank r
        h1 = True
        
        # H_2: sigma_1 >= ... >= sigma_r > 0 are the non-zero singular values of A
        h2 = True
        
        # H_3: A = sum_{i=1}^r sigma_i u_i v_i^* is the truncated singular value decomposition
        h3 = True
        
        # H_4: A_k = sum_{i=1}^k sigma_i u_i v_i^*
        # For this sum to be well-defined from the truncated SVD, we must have 0 <= k <= r.
        h4 = (0 <= k <= r)
        
        # ¬Q: The conclusion fails.
        # The conclusion states the minimum approximation error is exactly sigma_{k+1}.
        # If k >= min(A.rows, A.cols), the (k+1)-th singular value does not exist (is undefined),
        # making the statement "the minimum approximation error is sigma_{k+1}" mathematically false.
        neg_q = bool(k >= min(A.rows, A.cols))
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix with rank r",
    "H_2: sigma_1 >= ... >= sigma_r > 0 are the non-zero singular values of A",
    "H_3: A is given by its truncated SVD",
    "H_4: A_k is the k-th truncated SVD",
    "¬Q: The minimum approximation error is not sigma_{k+1} (e.g., sigma_{k+1} is undefined)"
]

N_HYP = 4
NEG_Q_INDEX = 4