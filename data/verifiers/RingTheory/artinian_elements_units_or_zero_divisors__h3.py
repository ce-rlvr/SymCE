import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a commutative ring with identity, every element is either a unit or a zero divisor."
    (This is true for Artinian rings, but false in general, e.g., in Z).
    """
    try:
        # The witness can be a tuple (Ring, element) or just the element (defaulting to ZZ)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, val = witness
        else:
            R = ZZ
            val = witness
            
        # Map common SymPy sets to their corresponding Poly domains for rigorous algebraic checks
        if R == sympy.S.Integers:
            R = ZZ
        elif R == sympy.S.Reals:
            R = RR
        elif R == sympy.S.Complexes:
            R = CC
        elif R == sympy.S.Rationals:
            R = QQ
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = False
        if R in [ZZ, QQ, RR, CC]:
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
    except Exception:
        h1 = False

    # H_2: R has a multiplicative identity
    try:
        h2 = False
        if R in [ZZ, QQ, RR, CC]:
            h2 = True
        elif hasattr(R, 'one') and R.one is not None:
            h2 = True
    except Exception:
        h2 = False

    # H_3: x is an element of R
    try:
        h3 = False
        if R in [ZZ, QQ, RR, CC]:
            h3 = bool(val in R)
        elif hasattr(R, '__contains__'):
            h3 = bool(val in R)
    except Exception:
        h3 = False

    # ¬Q: x is neither a unit nor a zero divisor
    try:
        # Check if val is a unit
        is_unit = True  # Default to True to fail-safe (reject unknown rings)
        if R == ZZ:
            is_unit = bool(val == 1 or val == -1)
        elif R in [QQ, RR, CC]:
            is_unit = bool(val != 0 and val != getattr(R, 'zero', 0))
        elif hasattr(R, 'exquo'):
            try:
                R.exquo(R.one, val)
                is_unit = True
            except Exception:
                is_unit = False

        # Check if val is a zero divisor
        is_zero_divisor = True  # Default to True to fail-safe
        if R in [ZZ, QQ, RR, CC]:
            is_zero_divisor = bool(val == 0 or val == getattr(R, 'zero', 0))
        elif hasattr(R, 'is_IntegralDomain') and R.is_IntegralDomain:
            is_zero_divisor = bool(val == 0 or val == getattr(R, 'zero', 0))

        neg_q = (not is_unit) and (not is_zero_divisor)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: x is an element of R",
    "¬Q: x is neither a unit nor a zero divisor"
]

N_HYP = 3
NEG_Q_INDEX = 3