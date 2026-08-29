import sympy
from sympy import Poly, gcd

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    try:
        f, c = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a unique factorization domain (c in R)
    # We use R = Z (the integers) as our UFD.
    try:
        c_sym = sympy.sympify(c)
        h1 = c_sym.is_integer
    except Exception:
        h1 = False
        
    # H_2: f is a non-zero polynomial with content d
    try:
        poly_f = Poly(f, x, domain='ZZ')
        h2 = not poly_f.is_zero
    except Exception:
        h2 = False
        
    # neg_Q: The greatest common divisor of f and c is NOT equal to 
    # the greatest common divisor of d and c, up to associates.
    try:
        poly_f = Poly(f, x, domain='ZZ')
        d = poly_f.content()
        
        # Compute GCDs
        gcd_fc = gcd(f, c)
        gcd_dc = gcd(d, c)
        
        # Convert to polynomials over Z to check for associates
        poly_gcd_fc = Poly(gcd_fc, x, domain='ZZ')
        poly_gcd_dc = Poly(gcd_dc, x, domain='ZZ')
        
        # In Z[x], the only units are 1 and -1, so associates differ at most by a sign.
        are_associates = (poly_gcd_fc == poly_gcd_dc) or (poly_gcd_fc == -poly_gcd_dc)
        neg_q = not are_associates
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: f is a non-zero polynomial over R with content d",
    "¬Q: GCD of f and c is not equal to GCD of d and c up to associates"
]

N_HYP = 2
NEG_Q_INDEX = 2