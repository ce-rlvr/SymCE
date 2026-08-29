import sympy
import math
from sympy import Rational, Integer

# Top-level setup: named object bindings
# No special group or linear algebra objects needed for this Number Theory conjecture.
# The witness is expected to be a tuple (a, b, c, m).

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    
    Hypotheses:
      H1: c is a positive integer
      H2: a \equiv b \pmod m
      
    Conclusion:
      Q: ac \equiv bc \pmod{mc}
    """
    try:
        # Unpack the witness
        a, b, c, m = witness
    except Exception:
        return [False, False, False]

    # H1: c is a positive integer
    try:
        # Check if c is an integer and strictly positive
        h1_ok = (isinstance(c, int) or (hasattr(c, 'is_integer') and c.is_integer)) and c > 0
    except Exception:
        h1_ok = False

    # H2: a \equiv b \pmod m
    try:
        if m == 0:
            h2_ok = (a == b)
        else:
            # Mathematically, a \equiv b \pmod m means m divides (a - b)
            h2_ok = ((a - b) % m) == 0
    except Exception:
        h2_ok = False

    # ¬Q: ac \equiv bc \pmod{mc} must FAIL
    try:
        mc = m * c
        if mc == 0:
            q_holds = (a * c == b * c)
        else:
            q_holds = ((a * c - b * c) % mc) == 0
            
        neg_q_ok = not q_holds
    except Exception:
        # If evaluating the conclusion raises an error, we consider it as failing to hold.
        neg_q_ok = True

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: c is a positive integer",
    "H_2: a ≡ b (mod m)",
    "¬Q: ac ≢ bc (mod mc)"
]

N_HYP = 2
NEG_Q_INDEX = 2