import sympy
import math

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple (R, u, x) where:
      - R is a ring (either an integer n >= 2 representing Z/nZ, or a SymPy domain like ZZ)
      - u is an element of R
      - x is an element of R
    """
    try:
        R, u, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a commutative ring
    try:
        if isinstance(R, int) and R >= 2:
            h1 = True
        elif hasattr(R, 'is_unit'):
            # SymPy domains (ZZ, QQ, etc.) are commutative rings
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: R has a multiplicative identity
    try:
        if isinstance(R, int) and R >= 2:
            h2 = True
        elif hasattr(R, 'is_unit'):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: u is a unit in R
    try:
        if isinstance(R, int) and R >= 2:
            h3 = (math.gcd(int(u) % R, R) == 1)
        elif hasattr(R, 'is_unit'):
            h3 = bool(R.is_unit(u))
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: u + x is not a unit in R
    try:
        if isinstance(R, int) and R >= 2:
            neg_q = (math.gcd(int(u + x) % R, R) != 1)
        elif hasattr(R, 'is_unit'):
            neg_q = not bool(R.is_unit(u + x))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: u is a unit in R",
    "¬Q: u + x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3