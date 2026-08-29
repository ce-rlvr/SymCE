import sympy
from sympy import symbols, Rational, Integer

# Top-level setup
class InfiniteNilIdealRing:
    """
    Represents a commutative ring R with an ideal I such that every element
    in I is nilpotent, but I itself is not nilpotent.
    Example: R = k[x_1, x_2, ...] / <x_1^2, x_2^2, ...> and I = <x_1, x_2, ...>.
    """
    def is_commutative_ring(self):
        return True

    def is_nil_ideal(self):
        return True

    def is_nilpotent_ideal(self):
        return False

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample.
    The witness can be an instance of InfiniteNilIdealRing, a custom object
    with the required methods/properties, or a dictionary.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_commutative_ring", False))
            h2 = bool(witness.get("is_nil_ideal", False))
            neg_q = not bool(witness.get("is_nilpotent_ideal", True))
        else:
            if hasattr(witness, "is_commutative_ring"):
                attr = witness.is_commutative_ring
                h1 = bool(attr() if callable(attr) else attr)
                
            if hasattr(witness, "is_nil_ideal"):
                attr = witness.is_nil_ideal
                h2 = bool(attr() if callable(attr) else attr)
                
            if hasattr(witness, "is_nilpotent_ideal"):
                attr = witness.is_nilpotent_ideal
                neg_q = not bool(attr() if callable(attr) else attr)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Every element x \\in I is nilpotent",
    "¬Q: I is not nilpotent (for all k > 0, I^k != {0})"
]

N_HYP = 2
NEG_Q_INDEX = 2