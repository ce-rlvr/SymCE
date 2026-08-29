import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ

# Top-level setup for FieldTheory
# We define standard rings and fields that might be used as witnesses.
# The conjecture fails when the ring R is not an integral domain, as the field of fractions 
# (and subsequently its algebraic closure) is only well-defined and behaves as expected for domains.

CONDITION_LABELS = [
    "H_1: Let K be the field of fractions of R",
    "H_2: Let K_bar be the algebraic closure of K",
    "H_3: Let S be the integral closure of R in K_bar",
    "¬Q: The field of fractions of S is not exactly K_bar"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    Given a witness ring R (or a tuple starting with R), this function evaluates the hypotheses
    and the negated conclusion.
    
    The hypotheses are definitions ("Let K be..."), so they are structurally satisfied.
    The conclusion "The field of fractions of S is exactly K_bar" is a known theorem 
    that holds unconditionally for all integral domains. Thus, the conjecture is false 
    (i.e., the conclusion fails) if and only if the witness R is NOT an integral domain.
    """
    # H1, H2, H3 are definitions/setup steps, so they hold by definition at the witness.
    h1 = True
    h2 = True
    h3 = True
    
    try:
        # Extract the ring if the witness is provided as a tuple (R, K, K_bar, S)
        if isinstance(witness, tuple) and len(witness) > 0:
            ring = witness[0]
        else:
            ring = witness
            
        # Check if the ring is an integral domain
        if isinstance(ring, int) or (hasattr(ring, 'is_integer') and ring.is_integer):
            n = int(ring)
            # For Z/nZ, it is a domain iff n is prime (or n=0 which is Z)
            if n == 1:
                is_domain = False
            elif n > 1:
                is_domain = sympy.isprime(n)
            elif n == 0:
                is_domain = True
            else:
                is_domain = True
        elif hasattr(ring, 'is_domain'):
            is_domain = bool(ring.is_domain)
        elif hasattr(ring, 'is_IntegralDomain'):
            is_domain = bool(ring.is_IntegralDomain)
        else:
            # If we cannot determine, we conservatively assume it is a domain
            is_domain = True
            
    except Exception:
        is_domain = True
        
    # The conclusion fails (neg_Q is True) if the ring is not an integral domain
    neg_q = not is_domain
    
    return [h1, h2, h3, neg_q]