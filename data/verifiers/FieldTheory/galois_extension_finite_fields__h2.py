import sympy
import math
from sympy.abc import x, y, z, t

# Top-level setup
# No specific named groups or matrices are strictly required for this field theory theorem.
# Symbols x, y, z, t are available for constructing fraction fields.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Every extension of a finite field is a Galois extension."
    (The dropped hypothesis is that the extension must be finite).
    
    The witness should be a tuple (E, F) where F is a finite field and E is a field extension of F.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        E, F = witness
    except Exception:
        return [False, False]
        
    # H1: F is a finite field
    try:
        h1 = type(F).__name__ in ('FiniteField', 'GaloisField') or \
             (hasattr(F, 'order') and hasattr(F, 'characteristic') and F.characteristic > 0)
        h1 = bool(h1)
    except Exception:
        h1 = False
        
    # neg_Q: E is NOT a Galois extension of F
    try:
        is_extension = False
        is_galois = False
        
        type_E = type(E).__name__
        type_F = type(F).__name__
        
        # Case 1: E is a finite field
        if type_E in ('FiniteField', 'GaloisField') and type_F in ('FiniteField', 'GaloisField'):
            if getattr(E, 'characteristic', None) == getattr(F, 'characteristic', None):
                try:
                    k = round(math.log(float(E.order), float(F.order)))
                    if F.order ** k == E.order:
                        is_extension = True
                        # Any finite extension of a finite field is Galois
                        is_galois = True
                except Exception:
                    pass
                    
        # Case 2: E is a fraction field (transcendental extension)
        elif type_E == 'FractionField' and getattr(E, 'domain', None) == F:
            is_extension = True
            # A transcendental extension of a finite field is never Galois
            # (the fixed field of its automorphism group is strictly larger than F)
            is_galois = False
            
        # Case 3: E is an algebraic field extension
        elif type_E == 'AlgebraicField' and getattr(E, 'domain', None) == F:
            is_extension = True
            # Algebraic extensions of finite fields are Galois
            is_galois = True
            
        if not is_extension:
            # If E is not a valid field extension of F, it's not a proper witness
            neg_q = False
        else:
            neg_q = not is_galois
            
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "¬Q: E is not a Galois extension of F"
]

N_HYP = 1
NEG_Q_INDEX = 1