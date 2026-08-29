import sympy
from sympy import Integer

# Top-level setup
# (No specific named bindings required for this field theory witness)

def conditions(witness) -> list[bool]:
    try:
        # Check if witness is a positive integer
        if isinstance(witness, (int, Integer)):
            h1 = int(witness) > 0
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # The conclusion is that Q(zeta_n)/Q is a Galois extension.
        # For any positive integer n, Q(zeta_n) is the splitting field of x^n - 1 over Q.
        # In characteristic 0, all extensions are separable.
        # A splitting field is a normal extension.
        # A finite, normal, separable extension is Galois.
        # Therefore, if n is a positive integer, the extension is ALWAYS Galois.
        if h1:
            is_galois = True
        else:
            is_galois = False
            
        neg_q = not is_galois
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The field extension Q(zeta_n)/Q is not a Galois extension"
]

N_HYP = 1
NEG_Q_INDEX = 1