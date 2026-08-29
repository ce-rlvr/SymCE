import sympy
from sympy import Poly, minpoly
from sympy.abc import x
from sympy.ntheory import factorint

def conditions(witness):
    """
    Checks if the witness represents an integral domain that is NOT integrally closed 
    in its field of fractions.
    
    The witness is expected to be either:
    1. A monic irreducible polynomial in x of degree 2 (e.g., x**2 - 5), representing ZZ[x]/(f(x)).
    2. An algebraic element (e.g., sqrt(5)), representing the ring ZZ[alpha].
    """
    try:
        # Try to interpret witness as a polynomial in x over ZZ
        p = Poly(witness, x, domain='ZZ')
    except Exception:
        try:
            # Try to interpret witness as an algebraic element and find its minimal polynomial
            p = Poly(minpoly(witness, x), x, domain='ZZ')
        except Exception:
            return [False]
            
    try:
        # The ring must be an integral domain, so the polynomial must be irreducible
        if not p.is_irreducible:
            return [False]
            
        # For simplicity and robustness, we restrict to quadratic extensions
        if p.degree() != 2:
            return [False]
            
        a, b, c = p.all_coeffs()
        
        # We expect a monic polynomial to form an order in the standard way
        if a != 1:
            return [False]
            
        # Discriminant of the polynomial (and thus of the order ZZ[alpha])
        D = b**2 - 4*a*c
        
        # Find the fundamental discriminant D_k of the number field Q(alpha)
        factors = factorint(abs(D))
        d = 1
        if D < 0:
            d = -1
            
        for p_prime, exp in factors.items():
            if exp % 2 == 1:
                d *= p_prime
        
        if d % 4 == 1:
            D_k = d
        else:
            D_k = 4 * d
        
        # The order is integrally closed iff its discriminant equals the fundamental discriminant
        is_int_closed = (D == D_k)
        
        # We want the conclusion to FAIL, meaning the ring is NOT integrally closed
        neg_q = not is_int_closed
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not integrally closed in its field of fractions"
]

N_HYP = 0
NEG_Q_INDEX = 0