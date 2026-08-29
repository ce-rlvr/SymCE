import sympy

def conditions(witness) -> list[bool]:
    try:
        k = sympy.sympify(witness)
        
        # If k is an integer, evaluate it exactly as a Python int
        try:
            if k == int(k):
                k = int(k)
        except Exception:
            pass
            
        m = 4 * k + 3
        
        try:
            # Compute the canonical modular inverse
            inv = sympy.mod_inverse(4, m)
            neg_q = bool(inv != k + 1)
        except Exception:
            # If mod_inverse fails (e.g., m is not an integer, or no inverse exists),
            # the conclusion that "the inverse is k+1" is false.
            neg_q = True
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of 4 modulo 4k + 3 is not k + 1"
]

N_HYP = 0
NEG_Q_INDEX = 0