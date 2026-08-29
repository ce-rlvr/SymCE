import sympy

def conditions(witness) -> list[bool]:
    try:
        a, b = int(witness[0]), int(witness[1])
    except Exception:
        return [False]
    
    try:
        # Calculate the modular inverse of a modulo a*b + 1
        inv = sympy.mod_inverse(a, a * b + 1)
        # The conclusion claims the inverse is exactly a*b - b + 1
        conclusion = (inv == a * b - b + 1)
    except Exception:
        # If mod_inverse fails (e.g., modulus is 0 or inverse does not exist),
        # the conclusion that the inverse is a*b - b + 1 is false.
        conclusion = False
        
    neg_q = not conclusion
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of a modulo ab+1 is not ab-b+1"
]

N_HYP = 0
NEG_Q_INDEX = 0