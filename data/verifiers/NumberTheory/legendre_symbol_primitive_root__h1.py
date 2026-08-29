import sympy
import sympy.ntheory

def conditions(witness):
    """
    Given a witness tuple (g, p), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        g, p = witness
    except Exception:
        return [False, False]
    
    # H_1: g is a primitive root modulo p
    try:
        h1 = bool(sympy.ntheory.is_primitive_root(g, p))
    except Exception:
        h1 = False
        
    # ¬Q: The Legendre symbol (g/p) is not equal to -1
    try:
        try:
            val = sympy.ntheory.legendre_symbol(g, p)
            neg_q = (val != -1)
        except ValueError:
            # If the Legendre symbol is undefined (e.g., p is not an odd prime),
            # then it is not equal to -1.
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: g is a primitive root modulo p",
    "¬Q: The Legendre symbol (g/p) is not equal to -1"
]

N_HYP = 1
NEG_Q_INDEX = 1