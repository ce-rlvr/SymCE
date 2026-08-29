import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        T, W = witness
    except Exception:
        return [False, False, False]
        
    try:
        T_mat = Matrix(T)
        
        try:
            if len(W) == 0:
                W_mat = zeros(T_mat.shape[0], 0)
            else:
                W_mat = Matrix(W)
        except TypeError:
            W_mat = Matrix(W)
            
        # If W was provided as a list of row vectors, transpose it to column vectors
        if W_mat.shape[0] != T_mat.shape[0] and W_mat.shape[1] == T_mat.shape[0]:
            W_mat = W_mat.T
            
        h1 = (T_mat.shape[0] == W_mat.shape[0])
    except Exception:
        h1 = False
        
    try:
        h2 = T_mat.is_square
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # The conclusion assumes W is T-invariant so that T|_W and the quotient operator are well-defined.
            # If W is not T-invariant, these operators are undefined, and the trace equality fails.
            W_rank = W_mat.rank()
            TW = T_mat * W_mat
            WTW = W_mat.row_join(TW)
            is_invariant = (WTW.rank() == W_rank)
            neg_q = not is_invariant
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: T is a linear operator on V",
    "¬Q: Trace equality fails (e.g., T|_W is undefined because W is not T-invariant)"
]

N_HYP = 2
NEG_Q_INDEX = 2