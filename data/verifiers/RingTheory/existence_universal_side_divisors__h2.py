import sympy
from sympy import QQ, ZZ
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If R is a Euclidean domain, then R contains at least one universal side divisor."
    
    A universal side divisor is defined as a non-zero non-unit element u in R such that 
    for every x in R, there exists a unit z or z=0 such that u divides x-z.
    Fields have no non-zero non-units, so they vacuously have no universal side divisors.
    Thus, any field is a valid counterexample.
    """
    # H_1: R is a Euclidean domain
    try:
        h1 = False
        # Fields are Euclidean domains
        if hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        # The integers are a Euclidean domain
        elif witness == ZZ:
            h1 = True
        # Polynomial rings over a field in one variable are Euclidean domains
        elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            if hasattr(witness.domain, 'is_Field') and witness.domain.is_Field and len(witness.symbols) == 1:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: R does NOT contain at least one universal side divisor
    try:
        # A universal side divisor must be a non-zero non-unit.
        # Fields have no non-zero non-units, so they cannot have a universal side divisor.
        if hasattr(witness, 'is_Field') and witness.is_Field:
            has_usd = False
        # Euclidean domains that are not fields always have a universal side divisor
        # (e.g., an element of minimal positive Euclidean norm).
        elif h1:
            has_usd = True
        else:
            has_usd = False
            
        neg_q = not has_usd
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: R does not contain at least one universal side divisor"
]

N_HYP = 1
NEG_Q_INDEX = 1