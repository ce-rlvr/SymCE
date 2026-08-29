import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup for Ring Theory / Number Theory
# The witness is expected to be an element (e.g., 1) or a tuple (R, p) where R is a domain.

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: p is a non-zero element of R",
    "H_3: p is a prime element of R",
    "¬Q: p is not an irreducible element of R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    
    The dropped hypothesis from the true theorem is "p is not a unit".
    Thus, a valid counterexample is a unit in an integral domain (e.g., p = 1 in ZZ),
    which vacuously satisfies the prime condition (p|ab => p|a or p|b) 
    but is not irreducible (since irreducible elements must be non-units).
    """
    # Unpack witness
    if isinstance(witness, tuple) and len(witness) == 2:
        R, p = witness
    else:
        R = ZZ
        p = witness

    # H_1: R is an integral domain
    try:
        if R == ZZ or R == QQ:
            h1 = True
        elif hasattr(R, 'is_domain'):
            h1 = bool(R.is_domain)
        elif hasattr(R, 'is_IntegralDomain'):
            h1 = bool(R.is_IntegralDomain)
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif type(R).__name__ in ('IntegerRing', 'RationalField', 'RealField', 'ComplexField', 'PolynomialRing', 'FractionField'):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: p is a non-zero element of R
    try:
        if hasattr(R, 'zero'):
            h2 = bool(p != R.zero and p != 0)
        else:
            h2 = bool(p != 0)
    except Exception:
        h2 = False

    # H_3: p is a prime element of R
    # In the context of the dropped hypothesis, units are considered prime 
    # because they vacuously satisfy the implication p|ab => p|a or p|b.
    try:
        h3 = False
        if R == ZZ:
            try:
                p_val = int(p)
                if p_val != 0:
                    if abs(p_val) == 1:
                        h3 = True
                    else:
                        h3 = sympy.isprime(abs(p_val))
            except Exception:
                pass
        
        if not h3:
            # Check if it's a unit in a general ring
            if hasattr(R, 'is_unit') and R.is_unit(p):
                h3 = True
            elif hasattr(R, 'is_prime'):
                h3 = bool(R.is_prime(p))
            elif hasattr(R, 'is_irreducible'):
                # In UFDs, irreducible implies prime
                h3 = bool(R.is_irreducible(p))
    except Exception:
        h3 = False

    # ¬Q: p is NOT an irreducible element of R
    # Irreducible elements are defined to be non-units.
    try:
        is_irred = False
        if R == ZZ:
            try:
                p_val = int(p)
                if p_val != 0 and abs(p_val) != 1:
                    is_irred = sympy.isprime(abs(p_val))
            except Exception:
                pass
        else:
            if hasattr(R, 'is_unit') and R.is_unit(p):
                is_irred = False
            elif hasattr(R, 'is_irreducible'):
                is_irred = bool(R.is_irreducible(p))
            elif hasattr(R, 'is_prime'):
                is_irred = bool(R.is_prime(p))
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]