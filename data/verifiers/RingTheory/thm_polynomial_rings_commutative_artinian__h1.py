import sympy

class NonNoetherianRing:
    is_Noetherian = False

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture:
    "If n is a positive integer, then the polynomial ring R in n variables is a Noetherian ring."
    
    The witness should be a tuple (R, n) or a dictionary {'R': R, 'n': n},
    where R is a ring (e.g., a custom object with `is_Noetherian = False`) and n is an integer.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            n = witness.get('n')
        else:
            R, n = witness
    except Exception:
        return [False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # neg_Q: R in n variables is NOT a Noetherian ring
    # By Hilbert's Basis Theorem, the polynomial ring is Noetherian iff R is Noetherian (for finite n).
    try:
        def is_noeth(ring):
            if hasattr(ring, 'is_Noetherian'):
                val = ring.is_Noetherian
                return bool(val() if callable(val) else val)
            if hasattr(ring, 'is_noetherian'):
                val = ring.is_noetherian
                return bool(val() if callable(val) else val)
            
            # Default to True so that counterexamples must be explicitly non-Noetherian
            return True
            
        neg_q = not is_noeth(R)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: the polynomial ring is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1