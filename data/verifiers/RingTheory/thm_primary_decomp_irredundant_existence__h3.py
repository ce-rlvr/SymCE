import sympy
from sympy import Rational, Integer, Symbol
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness can be an object with `ring.is_commutative`, `is_proper`, 
    and `has_primary_decomposition` attributes, or a dictionary containing 
    these boolean flags.
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_commutative_ring", False))
        else:
            h1 = bool(witness.ring.is_commutative)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get("is_proper_ideal", False))
        else:
            h2 = bool(witness.is_proper)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            # neg_q is True if it DOES NOT have a primary decomposition
            neg_q = not bool(witness.get("has_primary_decomposition", True))
        else:
            neg_q = not bool(witness.has_primary_decomposition)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: R is a commutative ring",
    "H_2: I is a proper ideal of R",
    "¬Q: I cannot be expressed as an irredundant finite intersection of primary ideals where the radicals of the primary components are distinct"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2