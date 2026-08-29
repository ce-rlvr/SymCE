import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # H_1: P is a matrix (duck-typing check for required matrix methods)
        h1 = hasattr(witness, 'pinv') and hasattr(witness, 'H') and hasattr(witness, 'is_square')
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            P = witness
            
            # Check if P is an orthogonal projection: must be square, idempotent, and Hermitian/symmetric
            if P.is_square:
                is_ortho_proj = bool((P**2 == P) and (P.H == P))
            else:
                is_ortho_proj = False
                
            # Check if P^+ = P
            P_plus = P.pinv()
            P_plus_equals_P = bool(P_plus == P)
            
            # The conclusion is the equivalence: P is an orthogonal projection iff P^+ = P
            # The negated conclusion means this equivalence fails (one is true and the other is false)
            neg_q = (is_ortho_proj != P_plus_equals_P)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a matrix",
    "¬Q: The equivalence (P is an orthogonal projection iff P^+ = P) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1