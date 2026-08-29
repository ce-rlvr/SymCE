import sympy

# Top-level setup
# (No named object bindings are required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Check if witness is an integer (excluding booleans)
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            a = int(witness)
            m = a**3 + 1
            v = a**3 - a**2 + 1
            
            # Evaluate if v is the strictly positive modular inverse of a modulo m
            if m == 0:
                q = False
            elif abs(m) == 1:
                # Modulo 1, the smallest strictly positive inverse is 1
                q = (v == 1)
            elif v <= 0 or v >= abs(m):
                # The strictly positive modular inverse must be in the range [1, |m|-1]
                q = False
            elif (a * v) % abs(m) != 1:
                # It must be a valid modular inverse
                q = False
            else:
                q = True
                
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "¬Q: The strictly positive modular inverse of a modulo a^3 + 1 is not a^3 - a^2 + 1"
]

N_HYP = 1
NEG_Q_INDEX = 1