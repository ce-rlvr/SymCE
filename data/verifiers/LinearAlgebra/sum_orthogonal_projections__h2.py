import sympy
from sympy import Matrix, zeros, eye

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            h1 = False
        else:
            P1, P2 = witness
            if (hasattr(P1, 'is_square') and hasattr(P2, 'is_square') and 
                P1.is_square and P2.is_square and P1.shape == P2.shape):
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    try:
        P1, P2 = witness
        n = P1.shape[0]
        Z = zeros(n, n)
        
        def is_ortho_proj(P):
            diff_idemp = (P**2 - P).expand()
            diff_selfadj = (P - P.H).expand()
            return diff_idemp == Z and diff_selfadj == Z
            
        sum_is_proj = is_ortho_proj(P1 + P2)
        prod_is_zero = (P1 * P2).expand() == Z
        
        neg_q = bool(sum_is_proj != prod_is_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space (witness is a pair of square matrices of the same size)",
    "¬Q: The equivalence (P1 + P2 is an orthogonal projection <=> P1 P2 = 0) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1