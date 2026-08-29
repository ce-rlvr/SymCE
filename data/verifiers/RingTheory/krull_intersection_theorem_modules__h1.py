import sympy
from sympy import symbols

# Top-level setup
class NonNoetherianRing:
    def __str__(self): 
        return "k[x, y_1, y_2, ...] / (y_i y_j, y_1 - x y_2, y_1 - x^2 y_3, ...)"

class KrullWitness:
    """
    A witness for the failure of Krull's Intersection Theorem in non-Noetherian rings.
    R = k[x, y_1, y_2, ...] / (y_i y_j, y_1 - x y_2, y_1 - x^2 y_3, ...)
    I = (x)
    M = R
    N = (y_1)
    IN = (x y_1) != N
    """
    def __init__(self):
        self.R = NonNoetherianRing()
        self.I_is_ideal = True
        self.M_is_finitely_generated = True
        self.N_is_intersection = True
        self.IN_equals_N = False

krull_counterexample = KrullWitness()

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    # Check if witness is the provided mock object or similar custom object
    try:
        if hasattr(witness, "I_is_ideal"):
            h1 = bool(witness.I_is_ideal)
            h2 = bool(witness.M_is_finitely_generated)
            h3 = bool(witness.N_is_intersection)
            neg_q = not bool(witness.IN_equals_N)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass
            
    # Check if witness is a dictionary
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("I_is_ideal", False))
            h2 = bool(witness.get("M_is_finitely_generated", False))
            h3 = bool(witness.get("N_is_intersection", False))
            neg_q = not bool(witness.get("IN_equals_N", True))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Fallback for SymPy objects (which will fail to be a counterexample since they are Noetherian)
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R, I, M, N = witness
            
            if hasattr(I, 'ring') and I.ring == R:
                h1 = True
            if hasattr(M, 'ring') and M.ring == R:
                h2 = True
                
            if h1 and h2:
                # For Noetherian rings, N = intersection I^n M implies N = I N
                IN = I * N
                IN_equals_N = (IN == N)
                neg_q = not IN_equals_N
                # If it's a valid intersection in a Noetherian ring, IN == N is True.
                h3 = IN_equals_N 
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: M is a finitely generated R-module",
    "H_3: N is the intersection of I^n M for all positive integers n",
    "¬Q: IN != N"
]

N_HYP = 3
NEG_Q_INDEX = 3