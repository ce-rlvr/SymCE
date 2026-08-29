import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def extract_witness(witness):
    if isinstance(witness, dict):
        T = witness.get('T')
        W = witness.get('W')
        lam = witness.get('lam')
    elif hasattr(witness, 'T') and hasattr(witness, 'W') and hasattr(witness, 'lam'):
        T = witness.T
        W = witness.W
        lam = witness.lam
    else:
        try:
            T, W, lam = witness
        except Exception:
            return None, None, None
            
    if not isinstance(T, sp.MatrixBase):
        try:
            T = sp.Matrix(T)
        except Exception:
            pass
            
    if not isinstance(W, sp.MatrixBase):
        try:
            if isinstance(W, list):
                if len(W) == 0:
                    if isinstance(T, sp.MatrixBase):
                        W = sp.zeros(T.shape[0], 0)
                elif all(isinstance(x, sp.MatrixBase) for x in W):
                    W = sp.Matrix.hstack(*W)
                else:
                    W = sp.Matrix(W)
            else:
                W = sp.Matrix(W)
        except Exception:
            pass
            
    try:
        lam = sp.sympify(lam)
    except Exception:
        pass
        
    return T, W, lam

def conditions(witness) -> list[bool]:
    try:
        extracted = extract_witness(witness)
        if extracted == (None, None, None):
            return [False, False, False, False]
        T, W, lam = extracted
    except Exception:
        return [False, False, False, False]
        
    # H1: V is a finite-dimensional vector space over a field F
    try:
        h1 = isinstance(T, sp.MatrixBase) and T.is_square
    except Exception:
        h1 = False
        
    # H2: T is a linear operator on V
    try:
        h2 = isinstance(T, sp.MatrixBase) and T.is_square and isinstance(W, sp.MatrixBase) and W.shape[0] == T.shape[0]
    except Exception:
        h2 = False
        
    # H3: \lambda is an eigenvalue of the induced quotient operator T/W
    # This means there exists v \notin W such that T(v) - \lambda v \in W
    try:
        n = T.shape[0]
        A = T - lam * sp.eye(n)
        # We want to find if there is v such that A*v = W*x for some x, and v not in W.
        # Solve [A, -W] * [v; x] = 0
        M = A.row_join(-W)
        null_basis = M.nullspace()
        
        h3 = False
        W_rank = W.rank()
        for vec in null_basis:
            v = vec[:n, :]
            if W.row_join(v).rank() > W_rank:
                h3 = True
                break
    except Exception:
        h3 = False
        
    # ¬Q: \lambda is NOT an eigenvalue of T
    try:
        n = T.shape[0]
        A = T - lam * sp.eye(n)
        det_val = A.det()
        is_eigenval = bool(sp.simplify(det_val) == 0)
        neg_q = not is_eigenval
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T is a linear operator on V",
    "H_3: lambda is an eigenvalue of the induced quotient operator T/W",
    "¬Q: lambda is not an eigenvalue of the operator T"
]

N_HYP = 3
NEG_Q_INDEX = 3