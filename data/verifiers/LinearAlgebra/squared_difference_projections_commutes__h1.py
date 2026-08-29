import sympy
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        P, Q = witness
        diff_sq = (P - Q)**2
        
        comm_P = diff_sq * P - P * diff_sq
        comm_Q = diff_sq * Q - Q * diff_sq
        
        def is_zero(expr):
            if hasattr(expr, 'is_zero_matrix'):
                res = expr.is_zero_matrix
                if res is not None:
                    return res
                return sympy.simplify(expr) == zeros(*expr.shape)
            return sympy.simplify(expr) == 0

        commutes_P = is_zero(comm_P)
        commutes_Q = is_zero(comm_Q)
        
        neg_q = not (commutes_P and commutes_Q)
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: (P-Q)^2 does not commute with both P and Q"
]

N_HYP = 0
NEG_Q_INDEX = 0