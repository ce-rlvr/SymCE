import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        U, P = witness
        U = sp.Matrix(U)
        P = sp.Matrix(P)
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = U.is_square
    except Exception:
        h1 = False
        
    try:
        if h1:
            n = U.shape[0]
            diff = U * U.H - sp.eye(n)
            diff = diff.applyfunc(sp.simplify)
            h2 = all(diff[i, j] == 0 for i in range(n) for j in range(n))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        h3 = P.is_square and P.shape == U.shape
    except Exception:
        h3 = False
        
    try:
        if h1 and h3:
            n = U.shape[0]
            M = U * P * U.H
            M = M.applyfunc(sp.simplify)
            diff1 = M**2 - M
            diff1 = diff1.applyfunc(sp.simplify)
            diff2 = M.H - M
            diff2 = diff2.applyfunc(sp.simplify)
            is_proj = all(diff1[i, j] == 0 for i in range(n) for j in range(n)) and \
                      all(diff2[i, j] == 0 for i in range(n) for j in range(n))
            neg_q = not is_proj
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "H_2: U is a unitary matrix",
    "H_3: P is an n x n complex matrix",
    "¬Q: U P U^* is not an orthogonal projection matrix"
]

N_HYP = 3
NEG_Q_INDEX = 3