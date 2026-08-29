import sympy
from sympy.matrices import eye, zeros, Matrix

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        P1, P2 = witness
    except Exception:
        return [False, False]

    # H_1: V is a vector space over a field of characteristic not equal to 2.
    # We verify this by checking that P1 and P2 are square matrices of the same size.
    try:
        h1 = (hasattr(P1, 'is_square') and P1.is_square and 
              hasattr(P2, 'is_square') and P2.is_square and 
              P1.shape == P2.shape)
    except Exception:
        h1 = False

    # ¬Q: The conclusion FAILS.
    # Conclusion: P_1 + P_2 is a projection operator if and only if P_1 P_2 = 0 and P_2 P_1 = 0.
    # Negation: (P_1 + P_2 is a projection) XOR (P_1 P_2 = 0 and P_2 P_1 = 0)
    try:
        if not h1:
            neg_q = False
        else:
            P_sum = P1 + P2
            is_proj_sum = ((P_sum * P_sum) == P_sum)
            
            prod1 = P1 * P2
            prod2 = P2 * P1
            Z = zeros(P1.rows, P1.cols)
            
            is_ortho = (prod1 == Z) and (prod2 == Z)
            
            neg_q = bool(is_proj_sum != is_ortho)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field of characteristic not equal to 2 (P1, P2 are square matrices of same size)",
    "¬Q: (P_1 + P_2 is a projection) is not equivalent to (P_1 P_2 = 0 and P_2 P_1 = 0)"
]

N_HYP = 1
NEG_Q_INDEX = 1