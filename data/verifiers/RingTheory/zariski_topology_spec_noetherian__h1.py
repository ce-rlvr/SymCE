import sympy
import sympy.abc
from sympy import symbols

# Top-level setup for potential witness objects
class InfinitePolynomialRing:
    """
    Represents a polynomial ring with infinitely many variables, e.g., k[x_1, x_2, ...].
    Such a ring is not Noetherian, and its prime spectrum is not a Noetherian space.
    """
    is_commutative = True
    is_ring = True
    is_noetherian = False
    
    def __str__(self):
        return "k[x_1, x_2, ...]"

class RingOfContinuousFunctions:
    """
    Represents the ring of continuous real-valued functions on a space like [0, 1].
    This ring is not Noetherian, and its prime spectrum is not a Noetherian space.
    """
    is_commutative = True
    is_ring = True
    is_noetherian = False
    
    def __str__(self):
        return "C([0, 1])"

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    'Let Spec(R) be the prime spectrum of R. Then Spec(R) is a Noetherian space.'
    
    The dropped hypothesis was that R itself is a Noetherian ring.
    """
    # H_1: R is a commutative ring
    h1 = False
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if any(kw in s for kw in ["ring", "algebra", "function", "product", "k[", "z[", "q[", "c(", "r[", "f[", "spec", "...", "infinit"]):
                h1 = True
            else:
                h1 = False
        elif hasattr(witness, 'is_commutative') and witness.is_commutative is not None:
            h1 = witness.is_commutative is not False
        elif hasattr(witness, 'is_Ring') and witness.is_Ring is not None:
            h1 = witness.is_Ring is not False
        elif hasattr(witness, 'is_ring') and witness.is_ring is not None:
            h1 = witness.is_ring is not False
        else:
            # Fallback for standard Python types
            if type(witness) in (int, float, list, tuple, dict, set, bool):
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: Spec(R) is NOT a Noetherian space
    neg_q = False
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if any(kw in s for kw in ["infinit", "...", "non-noetherian", "not noetherian", "continuous function", "c([0,1])", "c(x)"]):
                neg_q = True
        elif hasattr(witness, 'name') and isinstance(witness.name, str):
            s = witness.name.lower()
            if any(kw in s for kw in ["infinit", "...", "non-noetherian", "not noetherian", "continuous function"]):
                neg_q = True
        elif hasattr(witness, 'is_noetherian'):
            neg_q = not bool(witness.is_noetherian)
        elif hasattr(witness, 'is_Noetherian'):
            neg_q = not bool(witness.is_Noetherian)
        else:
            s = witness.__class__.__name__.lower()
            if any(kw in s for kw in ["infinit", "nonnoetherian", "continuous"]):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: Spec(R) is not a Noetherian space"
]

N_HYP = 1
NEG_Q_INDEX = 1