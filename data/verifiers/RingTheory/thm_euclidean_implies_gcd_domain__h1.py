import sympy
import sympy.polys
import sympy.abc
import math
import itertools
import functools

from sympy import Rational, Integer
from sympy.polys.domains import ZZ, QQ, EX

# Top-level setup
x, y, z = sympy.abc.x, sympy.abc.y, sympy.abc.z

N_HYP = 0
NEG_Q_INDEX = 0

CONDITION_LABELS = [
    "¬Q: R is not a GCD domain"
]

def _check_is_gcd(obj):
    """Helper to check if an object explicitly declares itself as a GCD/UFD domain."""
    for attr in ['is_GCD', 'is_gcd_domain', 'is_UFD', 'is_ufd']:
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            return bool(val() if callable(val) else val)
    return None

def conditions(witness) -> list[bool]:
    try:
        # The witness could be a ring R, or a tuple (R, a, b) where a and b have no GCD in R.
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
            is_gcd = _check_is_gcd(R)
            
            if is_gcd is None:
                if hasattr(R, 'gcd'):
                    try:
                        g = R.gcd(a, b)
                        is_gcd = True
                    except Exception:
                        # gcd computation failed, implying no GCD exists
                        is_gcd = False
                else:
                    # Unrecognized object without gcd method, assume True to avoid false positives
                    is_gcd = True
            elif is_gcd is True:
                # Explicitly a GCD domain, but let's verify the specific pair if possible
                if hasattr(R, 'gcd'):
                    try:
                        g = R.gcd(a, b)
                    except Exception:
                        is_gcd = False
        else:
            is_gcd = _check_is_gcd(witness)
            if is_gcd is None:
                # Unrecognized object, assume True to avoid false positives
                is_gcd = True
                
        neg_q = not is_gcd
    except Exception:
        neg_q = False

    return [neg_q]