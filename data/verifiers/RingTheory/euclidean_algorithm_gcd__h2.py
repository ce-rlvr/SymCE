import sympy
from sympy import S
from sympy.abc import x, y, z
import math

# Top-level setup for potential witness expressions
Z = S.Integers
Q = S.Rationals

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: r is the last non-zero remainder produced by the Euclidean algorithm applied to a and b",
    "¬Q: r is not a greatest common divisor of a and b"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_euclidean_domain(R):
    if R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
        return True
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        if R.domain.is_Field and len(R.symbols) == 1:
            return True
    if isinstance(R, sympy.polys.rings.PolyRing):
        if R.domain.is_Field and len(R.gens) == 1:
            return True
    return False

def get_last_nonzero_remainder(R, a, b):
    prev, curr = a, b
    last_nonzero = None
    
    def is_zero(val):
        if hasattr(val, 'is_zero') and val.is_zero is not None:
            return val.is_zero
        return val == 0 or val == getattr(R, 'zero', 0)

    steps = 0
    while not is_zero(curr):
        steps += 1
        if steps > 1000:
            raise ValueError("Euclidean algorithm did not terminate")
            
        if R == S.Integers or isinstance(prev, int):
            q, rem = divmod(prev, curr)
        elif hasattr(R, 'div'):
            q, rem = R.div(prev, curr)
        elif hasattr(prev, 'div'):
            q, rem = prev.div(curr)
        else:
            q, rem = divmod(prev, curr)
            
        if not is_zero(rem):
            last_nonzero = rem
        prev, curr = curr, rem
        
    return last_nonzero

def is_gcd(R, a, b, r):
    def is_zero(val):
        if hasattr(val, 'is_zero') and val.is_zero is not None:
            return val.is_zero
        return val == 0 or val == getattr(R, 'zero', 0)

    def divides(divisor, dividend):
        if is_zero(divisor):
            return is_zero(dividend)
        if R == S.Integers or isinstance(dividend, int):
            return dividend % divisor == 0
        elif hasattr(R, 'div'):
            q, rem = R.div(dividend, divisor)
            return is_zero(rem)
        elif hasattr(dividend, 'div'):
            q, rem = dividend.div(divisor)
            return is_zero(rem)
        else:
            return dividend % divisor == 0

    # r must be a common divisor
    if not (divides(r, a) and divides(r, b)):
        return False
        
    # r must be divisible by any other common divisor
    # In a PID, this is equivalent to r being an associate of the standard gcd
    if R == S.Integers or isinstance(a, int):
        return abs(int(r)) == math.gcd(int(a), int(b))
    elif hasattr(R, 'gcd'):
        g = R.gcd(a, b)
        return divides(r, g) and divides(g, r)
    elif hasattr(a, 'gcd'):
        g = a.gcd(b)
        return divides(r, g) and divides(g, r)
    else:
        return False

def conditions(witness):
    try:
        if len(witness) == 4:
            R, a, b, r = witness
        elif len(witness) == 3:
            a, b, r = witness
            R = S.Integers
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Euclidean domain
    try:
        h1 = bool(is_euclidean_domain(R))
    except Exception:
        h1 = False
        
    # H_2: r is the last non-zero remainder produced by the Euclidean algorithm applied to a and b
    try:
        last_rem = get_last_nonzero_remainder(R, a, b)
        h2 = (last_rem is not None) and (r == last_rem)
    except Exception:
        h2 = False
        
    # ¬Q: r is NOT a greatest common divisor of a and b
    try:
        neg_q = not is_gcd(R, a, b, r)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]