import sympy
from sympy import symbols, QQ, ZZ, CC, RR

# Top-level setup for witness evaluation
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    # H_1: F is a field
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, R = witness
        else:
            R = witness
            # If R is a polynomial ring, its base ring is R.domain
            if hasattr(R, 'domain'):
                F = R.domain
            else:
                F = R
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # ¬Q: R is not a Euclidean domain with respect to the degree function
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, R = witness
        else:
            R = witness
        
        # In sympy, Euclidean domains (like QQ[x]) are PIDs.
        # Polynomial rings in >= 2 variables (like QQ[x, y]) are not PIDs.
        if hasattr(R, 'is_PID'):
            is_euclidean = bool(R.is_PID)
        else:
            # Fallback: assume it is Euclidean to avoid false positives
            is_euclidean = True
            
        neg_q = not is_euclidean
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: R is not a Euclidean domain with respect to the degree function"
]

N_HYP = 1
NEG_Q_INDEX = 1