import sympy

# Top-level setup: named object bindings
class Ring:
    pass

class Ideal:
    pass

class DVR(Ring):
    """
    Represents the discrete valuation ring Z_{(p)}.
    """
    def __init__(self, p):
        self.p = p

    def is_valuation_ring(self):
        # A DVR is a valuation ring. We verify p is prime to ensure it's a valid Z_{(p)}.
        return sympy.isprime(self.p)

    def __eq__(self, other):
        return isinstance(other, DVR) and self.p == other.p

class DVRIdeal(Ideal):
    """
    Represents the ideal p^k Z_{(p)}.
    """
    def __init__(self, ring, k):
        self.ring = ring
        self.k = k

class Field(Ring):
    """
    Represents an arbitrary field.
    """
    def is_valuation_ring(self):
        # Every field is a valuation ring.
        return True

    def __eq__(self, other):
        return isinstance(other, Field)

class FieldIdeal(Ideal):
    """
    Represents an ideal in a field (either the zero ideal or the whole field).
    """
    def __init__(self, ring, is_zero):
        self.ring = ring
        self.is_zero = is_zero

def check_is_valuation_ring(ring):
    if hasattr(ring, 'is_valuation_ring'):
        return ring.is_valuation_ring()
    return False

def check_quotient_is_valuation_ring(ring, ideal):
    if isinstance(ring, DVR) and isinstance(ideal, DVRIdeal):
        # Z_{(p)} / p^k Z_{(p)} is a valuation ring iff it is an integral domain.
        # This happens if and only if k == 1 (giving the field Z/pZ).
        # If k == 0, it is the zero ring (not a domain).
        # If k > 1, it has zero divisors.
        return ideal.k == 1
    if isinstance(ring, Field) and isinstance(ideal, FieldIdeal):
        # Field / {0} is a field (valuation ring).
        # Field / Field is the zero ring (not a valuation ring).
        return ideal.is_zero
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a valuation ring, then the quotient ring R/I is a valuation ring."
    
    The witness should be a tuple (R, I).
    """
    try:
        R, I = witness
    except Exception:
        return [False, False]
        
    try:
        # H_1: R is a valuation ring and I is a valid ideal of R
        h1 = check_is_valuation_ring(R) and getattr(I, 'ring', None) == R
        if isinstance(I, DVRIdeal) and I.k < 0:
            h1 = False
    except Exception:
        h1 = False
        
    try:
        # neg_Q: The quotient ring R/I is NOT a valuation ring
        if getattr(I, 'ring', None) != R:
            neg_q = False
        else:
            neg_q = not check_quotient_is_valuation_ring(R, I)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a valuation ring",
    "¬Q: The quotient ring R/I is not a valuation ring"
]

N_HYP = 1
NEG_Q_INDEX = 1