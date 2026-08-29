import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import math

# Top-level setup
# The witness should be a list of tuples (a, b) representing the coefficients
# of a polynomial in Z[\sqrt{-5}][x].
# For example, the polynomial (6)x + (2 + 2\sqrt{-5}) is represented as:
# [(6, 0), (2, 2)]

def norm(val):
    return val[0]*val[0] + 5*val[1]*val[1]

def divides(d, val):
    if d == (0, 0):
        return val == (0, 0)
    num_0 = val[0]*d[0] + 5*val[1]*d[1]
    num_1 = -val[0]*d[1] + val[1]*d[0]
    den = d[0]*d[0] + 5*d[1]*d[1]
    return num_0 % den == 0 and num_1 % den == 0

def get_divisors(val):
    if val == (0, 0):
        return None
    n = norm(val)
    divs = set()
    max_a = int(math.isqrt(n))
    max_b = int(math.isqrt(n // 5)) if n >= 5 else 0
    for a in range(-max_a, max_a + 1):
        a2 = a * a
        for b in range(-max_b, max_b + 1):
            nd = a2 + 5 * b * b
            if nd != 0 and n % nd == 0:
                d = (a, b)
                if divides(d, val):
                    divs.add(d)
    return divs

def common_divisors(coeffs):
    c_divs = None
    for c in coeffs:
        if c == (0, 0):
            continue
        divs = get_divisors(c)
        if c_divs is None:
            c_divs = divs
        else:
            c_divs = c_divs.intersection(divs)
    if c_divs is None:
        return set()
    return c_divs

UNITS = {(1, 0), (-1, 0)}

def is_primitive(coeffs):
    c_divs = common_divisors(coeffs)
    return c_divs == UNITS

def exact_divide(val, d):
    num_0 = val[0]*d[0] + 5*val[1]*d[1]
    num_1 = -val[0]*d[1] + val[1]*d[0]
    den = d[0]*d[0] + 5*d[1]*d[1]
    return (num_0 // den, num_1 // den)

def conditions(witness):
    try:
        if not isinstance(witness, list) or not witness:
            return [False, False]
        if not all(isinstance(c, tuple) and len(c) == 2 for c in witness):
            return [False, False]
        if not all(isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) for a, b in witness):
            return [False, False]
        
        witness = [(int(a), int(b)) for a, b in witness]
        
        # H1: f is a non-zero polynomial
        h1 = any(c != (0, 0) for c in witness)
        
        if not h1:
            neg_q = False
        else:
            c_divs = common_divisors(witness)
            factorizations = 0
            for c in c_divs:
                f_star = [exact_divide(coeff, c) for coeff in witness]
                if is_primitive(f_star):
                    factorizations += 1
            
            # The representation is unique up to units iff there are exactly 2 factorizations
            # (since units are 1 and -1, each valid factorization gives exactly one other: -c, -f*)
            neg_q = (factorizations != 2)
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial in R",
    "¬Q: f does not have a unique content-primitive factorization up to units"
]

N_HYP = 1
NEG_Q_INDEX = 1