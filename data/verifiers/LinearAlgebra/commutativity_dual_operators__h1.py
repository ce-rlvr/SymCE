import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        S, T = witness
    except Exception:
        return [False, False, False]
        
    # H1: S and T are linear operators on V
    try:
        if hasattr(S, 'shape') and hasattr(T, 'shape'):
            h1 = len(S.shape) == 2 and S.shape[0] == S.shape[1] and S.shape == T.shape
        else:
            # For custom objects, assume they are valid linear operators if they can be unpacked
            h1 = True
    except Exception:
        h1 = False
        
    # H2: S o T = T o S
    try:
        if hasattr(S, 'shape') and hasattr(T, 'shape'):
            diff = S * T - T * S
            h2_val = diff.is_zero_matrix
            if h2_val is None:
                diff = sp.simplify(diff)
                h2_val = diff.is_zero_matrix
            h2 = False if h2_val is None else bool(h2_val)
        else:
            h2 = bool(S * T == T * S)
    except Exception:
        h2 = False
        
    # neg_Q: S^* o T^* != T^* o S^*
    try:
        def get_dual(op):
            if hasattr(op, 'dual'):
                return op.dual() if callable(op.dual) else op.dual
            if hasattr(op, 'adjoint'):
                return op.adjoint() if callable(op.adjoint) else op.adjoint
            if hasattr(op, 'T'):
                return op.T
            if hasattr(op, 'H'):
                return op.H
            raise ValueError("No dual operator found")
            
        S_star = get_dual(S)
        T_star = get_dual(T)
        
        if hasattr(S_star, 'shape') and hasattr(T_star, 'shape'):
            diff = S_star * T_star - T_star * S_star
            is_zero = diff.is_zero_matrix
            if is_zero is None:
                diff = sp.simplify(diff)
                is_zero = diff.is_zero_matrix
            neg_q = False if is_zero is None else not bool(is_zero)
        else:
            neg_q = bool(S_star * T_star != T_star * S_star)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S and T are linear operators on V",
    "H_2: S o T = T o S",
    "¬Q: S^* o T^* != T^* o S^*"
]

N_HYP = 2
NEG_Q_INDEX = 2