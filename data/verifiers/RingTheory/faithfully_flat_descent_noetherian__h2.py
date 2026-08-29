import sympy

class RingDef:
    def __init__(self, name, is_commutative, is_noetherian):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian
        
    def __repr__(self):
        return self.name

# Top-level setup: named object bindings that the witness expression may reference.
Z_ring = RingDef("Z", True, True)
Q_ring = RingDef("Q", True, True)
Poly_ring = RingDef("Q[x]", True, True)
Inf_poly_ring = RingDef("Q[x_1, x_2, ...]", True, False)
Weyl_algebra = RingDef("WeylAlgebra", False, True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R and S be commutative rings. If S is Noetherian, then R is Noetherian."
    
    The witness should be a tuple (R, S).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        R, S = witness
    except Exception:
        return [False, False, False]

    # H_1: R and S are commutative rings
    try:
        h1 = bool(getattr(R, 'is_commutative', False) and getattr(S, 'is_commutative', False))
    except Exception:
        h1 = False

    # H_2: S is a Noetherian ring
    try:
        h2 = bool(getattr(S, 'is_noetherian', False))
    except Exception:
        h2 = False

    # ¬Q: R is not a Noetherian ring
    try:
        # We check that R is explicitly NOT Noetherian.
        # If the attribute is missing, we default to True so neg_q becomes False (safe fallback).
        neg_q = not bool(getattr(R, 'is_noetherian', True))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: S is a Noetherian ring",
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2