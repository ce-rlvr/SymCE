import sympy
from sympy import Poly
from sympy.abc import x

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture.
    The conjecture claims that for a polynomial f over a UFD R, there is a unique 
    (up to units) representation f = c * f^* where c is in R and f^* is primitive.
    This fails exactly when f is the zero polynomial, because 0 = 0 * f^* for ANY 
    primitive polynomial f^*, and since there are primitive polynomials that are 
    not associates (e.g., x and x^2), uniqueness fails.
    """
    h1 = False
    neg_q = False
    
    try:
        # Ensure the witness is treated as a polynomial
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness, x, domain='ZZ')
            
        # H_1: R is a Unique Factorization Domain
        domain = f.domain
        if hasattr(domain, 'is_UFD'):
            h1 = bool(domain.is_UFD)
        else:
            # Fallback for domains that might not explicitly have the is_UFD property
            h1 = domain in (sympy.ZZ, sympy.QQ)
            
        # ¬Q: The representation f = c f^* is NOT unique up to multiplication by units.
        # As explained, this happens if and only if f is the zero polynomial.
        neg_q = bool(f.is_zero)
        
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: The representation f = c f^* is not unique up to multiplication by units of R"
]

N_HYP = 1
NEG_Q_INDEX = 1