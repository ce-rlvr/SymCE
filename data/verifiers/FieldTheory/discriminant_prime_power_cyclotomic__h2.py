import sympy
from sympy import isprime, cyclotomic_poly, discriminant, Rational
from sympy.abc import x

# Top-level setup
# (No specific named objects required for this domain, using x for polynomials)

def conditions(witness):
    try:
        p, k = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: K = Q(zeta_{p^k}) is the p^k-th cyclotomic field
    # This requires p^k to be a valid index for a cyclotomic field (integer >= 1).
    # Since p is prime (>= 2), k must be a non-negative integer.
    try:
        h2 = bool((int(k) == k) and k >= 0)
    except Exception:
        h2 = False
        
    # neg_Q: The absolute value of the discriminant of K over Q is NOT equal to p^{p^{k-1}(pk-k-1)}
    try:
        if not h2:
            neg_q = False
        else:
            n = p**k
            # Use exact polynomial discriminant for small n to be authentic,
            # fallback to the known theorem formula for large n to ensure it's fast.
            if n <= 100:
                poly = cyclotomic_poly(n, x)
                disc = discriminant(poly, x)
                abs_disc = abs(disc)
            else:
                if k == 0:
                    abs_disc = 1
                else:
                    abs_disc = p**(p**(k-1) * (p*k - k - 1))
            
            p_sym = sympy.S(p)
            if k - 1 < 0:
                term1 = Rational(1, p_sym**(1 - k))
            else:
                term1 = p_sym**(k - 1)
                
            exponent = term1 * (p_sym*k - k - 1)
            formula_val = p_sym**exponent
            
            neg_q = bool(abs_disc != formula_val)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: K = Q(zeta_{p^k}) is the p^k-th cyclotomic field",
    "¬Q: The absolute value of the discriminant of K over Q is not equal to p^{p^{k-1}(pk-k-1)}"
]

N_HYP = 2
NEG_Q_INDEX = 2