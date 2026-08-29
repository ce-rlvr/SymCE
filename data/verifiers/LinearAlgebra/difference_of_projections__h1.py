import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        P1, P2 = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: P_1 and P_2 are linear operators (represented as square matrices of the same size)
    try:
        h1 = (hasattr(P1, 'is_square') and hasattr(P2, 'is_square') and 
              P1.is_square and P2.is_square and P1.shape == P2.shape)
    except Exception:
        h1 = False

    # H_2: P_1^2 = P_1
    try:
        h2 = bool(P1 * P1 == P1)
    except Exception:
        h2 = False

    # H_3: P_2^2 = P_2
    try:
        h3 = bool(P2 * P2 == P2)
    except Exception:
        h3 = False

    # ¬Q: P_1 - P_2 is a projection operator if and only if P_1 P_2 = P_2 P_1 = P_2 (Negated)
    try:
        diff = P1 - P2
        is_proj_diff = bool(diff * diff == diff)
        is_comm_P2 = bool((P1 * P2 == P2) and (P2 * P1 == P2))
        
        # The conclusion is (is_proj_diff <==> is_comm_P2).
        # The negation is the XOR of the two sides.
        neg_q = is_proj_diff != is_comm_P2
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P_1 and P_2 are linear operators",
    "H_2: P_1^2 = P_1",
    "H_3: P_2^2 = P_2",
    "¬Q: (P_1 - P_2 is a projection) XOR (P_1 P_2 = P_2 P_1 = P_2)"
]

N_HYP = 3
NEG_Q_INDEX = 3