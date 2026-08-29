import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

# --- Top-level setup ---
# SymPy does not natively represent infinite direct products of rings, 
# which are the standard counterexamples for this conjecture.
# We provide wrapper classes and pre-defined instances that a witness expression may reference.

class InfiniteProductRing:
    """
    Represents an infinite direct product of a given base ring.
    """
    def __init__(self, base_ring):
        self.base_ring = base_ring

    def is_reduced(self):
        # An infinite product of reduced rings (like fields or integral domains) is reduced.
        return True

    def is_total_ring_of_fractions_finite_product_of_fields(self):
        # The total ring of fractions of an infinite product of fields/domains
        # is an infinite product of fields, which is NOT a finite product.
        return False

class FiniteProductRing:
    """
    Represents a finite direct product of given rings.
    """
    def __init__(self, *rings):
        self.rings = rings

    def is_reduced(self):
        return True

    def is_total_ring_of_fractions_finite_product_of_fields(self):
        return True

# Pre-defined common counterexamples
InfiniteBooleanRing = InfiniteProductRing(ZZ)
InfiniteProductOfFields = InfiniteProductRing(QQ)


def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: R is a reduced ring
    try:
        if hasattr(witness, 'is_reduced'):
            h1_ok = bool(witness.is_reduced())
        elif hasattr(witness, 'is_Domain') and witness.is_Domain:
            # SymPy integral domains are reduced
            h1_ok = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            # SymPy fields are reduced
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: The total ring of fractions of R is NOT isomorphic to a finite direct product of fields
    try:
        if hasattr(witness, 'is_total_ring_of_fractions_finite_product_of_fields'):
            q = bool(witness.is_total_ring_of_fractions_finite_product_of_fields())
        elif hasattr(witness, 'is_Domain') and witness.is_Domain:
            # For an integral domain, the total ring of fractions is its field of fractions (1 field)
            q = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            # A field is a finite product of 1 field
            q = True
        else:
            # Default fallback for unknown objects
            q = True
            
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]


CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "¬Q: The total ring of fractions of R is not isomorphic to a finite direct product of fields"
]

N_HYP = 1
NEG_Q_INDEX = 1