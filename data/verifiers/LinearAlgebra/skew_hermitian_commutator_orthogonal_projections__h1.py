import sympy
from sympy import eye, zeros
from sympy.matrices import Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        P, Q = witness
        M = P * Q - Q * P
        diff = M.H + M
        
        is_skew_hermitian = diff.is_zero_matrix
        if is_skew_hermitian is None:
            is_skew_hermitian = all(sympy.simplify(e) == 0 for e in diff)
            
        neg_q = not is_skew_hermitian
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = ["¬Q: PQ - QP is not skew-Hermitian"]
N_HYP = 0
NEG_Q_INDEX = 0