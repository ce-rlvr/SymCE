import sympy
from sympy import Rational, Integer
import math

# Top-level setup
# Number theory domain: no named bindings needed; use integers directly.

def is_int(val):
    """Safely check if a value is mathematically an integer."""
    try:
        if hasattr(val, 'is_integer'):
            if callable(val.is_integer):
                return bool(val.is_integer())
            elif val.is_integer is not None:
                return bool(val.is_integer)
        return int(val) == val
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            m = witness['m']
            x = witness['x']
        else:
            a, b, m, x = witness
    except Exception:
        return [False, False]

    # H_1: m > 0
    try:
        h1 = bool(m > 0)
    except Exception:
        h1 = False

    # neg_Q: ax \equiv b \pmod m is not equivalent to the existence of integer y such that ax - my = b
    try:
        # LHS: ax \equiv b \pmod m
        # The congruence notation is mathematically defined over integers.
        # If the variables are not integers, the congruence is undefined/false.
        lhs_valid = is_int(a) and is_int(x) and is_int(b) and is_int(m)
        if lhs_valid:
            lhs = ((a * x - b) % m == 0)
        else:
            lhs = False
        
        # RHS: there exists an integer y such that ax - my = b
        # This is algebraically equivalent to (ax - b) / m being an integer.
        rhs = is_int((a * x - b) / m)
        
        # The conclusion is LHS <==> RHS.
        # neg_Q is True if the conclusion FAILS (i.e., LHS and RHS have different truth values).
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m > 0",
    "¬Q: ax ≡ b (mod m) is not equivalent to the existence of integer y such that ax - my = b"
]

N_HYP = 1
NEG_Q_INDEX = 1