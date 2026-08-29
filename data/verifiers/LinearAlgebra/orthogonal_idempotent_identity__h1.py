import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_zero_matrix(M):
    n, m = M.shape
    for i in range(n):
        for j in range(m):
            val = M[i, j]
            if val != 0:
                val = sp.simplify(val)
                if val != 0:
                    return False
    return True

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if getattr(witness, 'is_square', False):
            n = int(witness.shape[0])
            diff1 = witness.T * witness - sp.eye(n)
            h1 = is_zero_matrix(diff1)
    except Exception:
        h1 = False
        
    try:
        if getattr(witness, 'is_square', False):
            n = int(witness.shape[0])
            diff2 = witness * witness - witness
            h2 = is_zero_matrix(diff2)
    except Exception:
        h2 = False
        
    try:
        if getattr(witness, 'is_square', False):
            n = int(witness.shape[0])
            diff3 = witness - sp.eye(n)
            neg_q = not is_zero_matrix(diff3)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "H_2: Q is an idempotent matrix (Q^2 = Q)",
    "¬Q: Q is not the n x n identity matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2