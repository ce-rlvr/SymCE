import sympy as sp
from sympy import eye, zeros

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_expr(e):
    try:
        if e == 0:
            return True
        if hasattr(e, 'is_zero') and e.is_zero is True:
            return True
        return False
    except Exception:
        return False

def matrix_eq(A, B):
    try:
        if A.shape != B.shape:
            return False
        diff = A - B
        if all(is_zero_expr(e) for e in diff):
            return True
        diff_exp = diff.expand()
        if all(is_zero_expr(e) for e in diff_exp):
            return True
        diff_simp = sp.simplify(diff)
        return all(is_zero_expr(e) for e in diff_simp)
    except Exception:
        return False

def is_orth_proj(P):
    try:
        if not hasattr(P, 'shape') or len(P.shape) != 2:
            return False
        if P.shape[0] != P.shape[1]:
            return False
        if not matrix_eq(P**2, P):
            return False
        if not matrix_eq(P, P.H):
            return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        P1_raw, P2_raw = witness
        P1 = sp.Matrix(P1_raw)
        P2 = sp.Matrix(P2_raw)
    except Exception:
        return [False, False, False]
    
    h1 = is_orth_proj(P1)
    h2 = is_orth_proj(P2)
    
    try:
        P12 = P1 * P2
        is_orth = is_orth_proj(P12)
        commutes = matrix_eq(P1 * P2, P2 * P1)
        
        # Conclusion Q: P_1 P_2 is an orthogonal projection iff P_1 P_2 = P_2 P_1
        q = (is_orth == commutes)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P_1 is an orthogonal projection",
    "H_2: P_2 is an orthogonal projection",
    "¬Q: The equivalence (P_1 P_2 is an orthogonal projection iff P_1 P_2 = P_2 P_1) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2