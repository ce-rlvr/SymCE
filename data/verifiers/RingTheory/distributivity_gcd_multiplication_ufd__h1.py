import sympy as sp
import math
from sympy.abc import *
from sympy import sqrt, I, Rational, Integer

# Top-level setup
# The standard counterexample for this theorem is in the ring Z[\sqrt{-5}].
# We provide standard sympy objects so the witness can be easily expressed.
# The witness should be a tuple of 4 expressions (a, b, c, d) in Z[\sqrt{-5}],
# or a tuple of 5 elements (D, a, b, c, d) for a general Z[\sqrt{D}] with D < 0.

def get_coeffs(expr, D):
    """Extracts (u, v) such that expr = u + v*sqrt(D). Returns None if not in Z[\sqrt{D}]."""
    if isinstance(expr, int):
        return (expr, 0)
    if isinstance(expr, tuple) and len(expr) == 2:
        return (int(expr[0]), int(expr[1]))
        
    if not hasattr(expr, 'as_independent'):
        return None
        
    expr = sp.expand(expr)
    if expr.is_Integer:
        return (int(expr), 0)
        
    sq = sp.sqrt(D)
    u, v_sq = expr.as_independent(sq, as_Add=True)
    v = sp.simplify(v_sq / sq)
    
    try:
        if u.is_Integer and v.is_Integer:
            return (int(u), int(v))
    except Exception:
        pass
    return None

def divides_Z_sqrt(x, y, D):
    """Checks if x divides y in Z[\sqrt{D}]."""
    u, v = x
    a, b = y
    det = u**2 - D * v**2
    if det == 0:
        return a == 0 and b == 0
    w_num = a * u - D * b * v
    z_num = b * u - a * v
    return w_num % det == 0 and z_num % det == 0

def get_all_divisors(x, D):
    """Returns a set of all divisors of x in Z[\sqrt{D}]."""
    if x == (0, 0):
        return set()
    
    N_x = x[0]**2 - D * x[1]**2
    divs = set()
    for i in range(1, int(math.isqrt(N_x)) + 1):
        if N_x % i == 0:
            divs.add(i)
            divs.add(N_x // i)
            
    abs_D = -D
    elements = set()
    for k in divs:
        max_z = int(math.isqrt(k // abs_D))
        for z in range(-max_z, max_z + 1):
            w2 = k - abs_D * z**2
            if w2 >= 0:
                w = int(math.isqrt(w2))
                if w * w == w2:
                    elements.add((w, z))
                    elements.add((-w, z))
                    
    actual_divisors = set()
    for e in elements:
        if divides_Z_sqrt(e, x, D):
            actual_divisors.add(e)
            
    return actual_divisors

def is_gcd(d, a, b, D):
    """Checks if d is a greatest common divisor of a and b in Z[\sqrt{D}]."""
    if not divides_Z_sqrt(d, a, D) or not divides_Z_sqrt(d, b, D):
        return False
    
    divs_a = get_all_divisors(a, D)
    divs_b = get_all_divisors(b, D)
    common_divs = divs_a.intersection(divs_b)
    
    for e in common_divs:
        if not divides_Z_sqrt(e, d, D):
            return False
    return True

def mul_Z_sqrt(x, y, D):
    """Multiplies two elements in Z[\sqrt{D}]."""
    u, v = x
    w, z = y
    return (u*w + D*v*z, u*z + v*w)

def conditions(witness):
    try:
        D = -5
        if len(witness) == 5:
            if isinstance(witness[0], int) and witness[0] < 0:
                D = witness[0]
                exprs = witness[1:]
            else:
                return [False, False, False]
        elif len(witness) == 4:
            exprs = witness
        else:
            return [False, False, False]
            
        a = get_coeffs(exprs[0], D)
        b = get_coeffs(exprs[1], D)
        c = get_coeffs(exprs[2], D)
        d = get_coeffs(exprs[3], D)
        
        if any(x is None for x in [a, b, c, d]):
            return [False, False, False]
            
        # H_1: a, b, and c are non-zero elements of R
        h1 = (a != (0, 0)) and (b != (0, 0)) and (c != (0, 0))
        
        # H_2: d is a greatest common divisor of a and b
        h2 = is_gcd(d, a, b, D)
        
        # Conclusion: The product cd is a greatest common divisor of ca and cb
        ca = mul_Z_sqrt(c, a, D)
        cb = mul_Z_sqrt(c, b, D)
        cd = mul_Z_sqrt(c, d, D)
        
        q = is_gcd(cd, ca, cb, D)
        
        return [bool(h1), bool(h2), not q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero elements of R",
    "H_2: d is a greatest common divisor of a and b",
    "¬Q: cd is not a greatest common divisor of ca and cb"
]

N_HYP = 2
NEG_Q_INDEX = 2