import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ

class AbstractRing:
    """
    A simple class to represent abstract rings with specific properties,
    since SymPy does not natively model properties like 'is_left_Noetherian'
    for arbitrary infinite-dimensional or non-Noetherian rings.
    """
    def __init__(self, name, is_ring=True, has_identity=True, is_left_Noetherian=True):
        self.name = name
        self.is_ring = is_ring
        self.has_identity = has_identity
        self.is_left_Noetherian = is_left_Noetherian
        
    def __str__(self):
        return self.name

# Named object bindings for the witness expression to reference
# A standard counterexample to the false conjecture is a polynomial ring 
# in infinitely many variables over a field, which is a ring with identity 
# but is not Noetherian.
Poly_inf = AbstractRing("k[X1, X2, ...]", is_ring=True, has_identity=True, is_left_Noetherian=False)

# Another counterexample: the ring of continuous real-valued functions on [0, 1]
C_0_1 = AbstractRing("C([0, 1], R)", is_ring=True, has_identity=True, is_left_Noetherian=False)

# A ring without identity (not a counterexample to this specific conjecture, but useful for testing)
EvenIntegers = AbstractRing("2Z", is_ring=True, has_identity=False, is_left_Noetherian=True)

def conditions(witness) -> list[bool]:
    # H_1: R is a ring
    try:
        if hasattr(witness, 'is_ring'):
            h1 = bool(witness.is_ring)
        elif hasattr(witness, 'is_Ring'):
            h1 = bool(witness.is_Ring)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: R has a multiplicative identity
    try:
        if hasattr(witness, 'has_identity'):
            h2 = bool(witness.has_identity)
        elif hasattr(witness, 'has_Identity'):
            h2 = bool(witness.has_Identity)
        elif hasattr(witness, 'one'):
            h2 = witness.one is not None
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: R is not a left Noetherian ring
    try:
        if hasattr(witness, 'is_left_Noetherian'):
            neg_q = not bool(witness.is_left_Noetherian)
        else:
            # Standard SymPy domains (ZZ, QQ, finite extensions, etc.) are Noetherian.
            # If the witness is a SymPy domain, it is Noetherian, so neg_q is False.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R has a multiplicative identity",
    "¬Q: R is not a left Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2