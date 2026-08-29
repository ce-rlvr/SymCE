import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_zero_matrix(M):
    """Helper function to robustly check if a SymPy matrix is zero."""
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            val = sp.simplify(M[i, j])
            if not (val == 0 or val.is_zero):
                return False
    return True

def conditions(witness):
    # Parse witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            P, r_wit = witness
        else:
            P = witness
            r_wit = None
            
        if not isinstance(P, sp.MatrixBase):
            P = sp.Matrix(P)
            
        if not P.is_square:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: P is an orthogonal projector, meaning P^2 = P and P = P*
    # We check both P == P.H (conjugate transpose) and P == P.T (transpose)
    # because the false conjecture arises when P* is interpreted as the transpose 
    # for complex matrices (dropping the "real matrix" hypothesis).
    try:
        diff_idemp = P**2 - P
        is_idemp = is_zero_matrix(diff_idemp)
        
        diff_H = P - P.H
        is_H = is_zero_matrix(diff_H)
        
        diff_T = P - P.T
        is_T = is_zero_matrix(diff_T)
        
        h1 = bool(is_idemp and (is_H or is_T))
    except Exception:
        h1 = False

    # H_2: Let r be the rank of P
    try:
        r = P.rank()
        if r_wit is not None:
            h2 = bool(r == r_wit)
        else:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: P does NOT have exactly r singular values equal to 1, and n - r singular values equal to 0
    try:
        n = P.shape[0]
        r = P.rank()
        svs = P.singular_values()
        
        ones = 0
        for sv in svs:
            diff = sp.simplify(sv - 1)
            if diff == 0 or diff.is_zero:
                ones += 1
                
        zeros = 0
        for sv in svs:
            diff = sp.simplify(sv)
            if diff == 0 or diff.is_zero:
                zeros += 1
                
        # In case SymPy omits zero singular values
        if len(svs) < n:
            zeros += n - len(svs)
            
        q = (ones == r) and (zeros == n - r)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is an orthogonal projector (P^2 = P and P = P*)",
    "H_2: r is the rank of P",
    "¬Q: P does not have exactly r singular values equal to 1 and n-r equal to 0"
]

N_HYP = 2
NEG_Q_INDEX = 2