import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Witness is expected to be a tuple or list of two SymPy matrices (S, T)
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
            
        S, T = witness
        
        # Ensure they are square matrices of the same dimension
        if not hasattr(S, 'shape') or not hasattr(T, 'shape'):
            return [False, False, False]
        if S.shape[0] != S.shape[1] or T.shape[0] != T.shape[1] or S.shape != T.shape:
            return [False, False, False]

        # H_1: S is a self-adjoint linear operator on V
        h1 = (S == S.H)
        
        # H_2: T is a self-adjoint linear operator on V
        h2 = (T == T.H)
        
        # Conclusion: The operator ST is self-adjoint if and only if ST = TS
        ST = S * T
        TS = T * S
        
        ST_is_self_adjoint = (ST == ST.H)
        ST_equals_TS = (ST == TS)
        
        q = (ST_is_self_adjoint == ST_equals_TS)
        neg_q = not q
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: S is a self-adjoint linear operator on V",
    "H_2: T is a self-adjoint linear operator on V",
    "¬Q: It is NOT the case that (ST is self-adjoint if and only if ST = TS)"
]

N_HYP = 2
NEG_Q_INDEX = 2