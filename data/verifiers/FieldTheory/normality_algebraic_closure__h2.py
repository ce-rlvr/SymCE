import sympy
import sympy.polys
from sympy.polys.domains import QQ, ZZ, RR, CC

# Top-level setup
# Define some common fields and rings for potential witnesses
Z2 = sympy.polys.domains.GF(2)
Z3 = sympy.polys.domains.GF(3)
Z5 = sympy.polys.domains.GF(5)

def conditions(witness) -> list[bool]:
    # H_1: F is a field
    try:
        if hasattr(witness, 'is_Field'):
            h1 = bool(witness.is_Field)
        elif hasattr(witness, 'is_field'):
            h1 = bool(witness.is_field)
        else:
            try:
                from sympy.polys.domains import Field
                h1 = isinstance(witness, Field)
            except ImportError:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: \bar{F} is not a normal extension of F
    try:
        # The algebraic closure of a field is mathematically always a normal extension.
        # Therefore, the conclusion "\bar{F} is a normal extension of F" is universally true
        # for any field F, and its negation is always False.
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: \\bar{F} is not a normal extension of F"
]

N_HYP = 1
NEG_Q_INDEX = 1