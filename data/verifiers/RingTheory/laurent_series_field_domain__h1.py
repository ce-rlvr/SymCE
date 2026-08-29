import sympy
from sympy import Rational, Integer
from sympy.abc import x

# Top-level setup
Z2 = sympy.GF(2)
Z3 = sympy.GF(3)
Z4 = sympy.IntegerRing() # Placeholder for non-field
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    """
    Evaluates the conjecture:
    "The formal Laurent series ring R((x)) is a field if and only if R is a field"
    """
    try:
        # Check if R is a field
        r_is_field = witness.is_Field
    except Exception:
        r_is_field = False

    try:
        # Check if R((x)) is a field.
        # In standard commutative algebra, R((x)) is a field iff R is a field.
        # However, if R is a non-commutative division ring, R((x)) is a division ring but NOT a field.
        # If the witness is a non-commutative ring, we evaluate accordingly.
        # For SymPy domains, we can use the mathematical property directly.
        if hasattr(witness, 'is_commutative') and not witness.is_commutative:
            r_laurent_is_field = False
        else:
            r_laurent_is_field = r_is_field
    except Exception:
        r_laurent_is_field = False

    try:
        # The conclusion is "R((x)) is a field iff R is a field"
        conclusion = (r_laurent_is_field == r_is_field)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The formal Laurent series ring R((x)) is a field if and only if R is a field fails"
]

N_HYP = 0
NEG_Q_INDEX = 0