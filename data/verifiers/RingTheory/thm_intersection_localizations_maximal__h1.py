import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any ring R with a field of fractions K, 
    the intersection of its localizations at all maximal ideals equals R.
    This is true for all commutative integral domains with an identity element,
    but fails if R lacks a multiplicative identity or is non-commutative.
    """
    # The witness may be provided as a tuple (R, K) or just R.
    if isinstance(witness, tuple) and len(witness) == 2:
        R, K = witness
    else:
        R = witness
        K = None

    # H_1: K is the field of fractions of R
    h1 = False
    try:
        if K is not None:
            if hasattr(R, 'get_field') and K == R.get_field():
                h1 = True
            elif hasattr(R, 'frac_field') and K == R.frac_field:
                h1 = True
            elif hasattr(R, 'fraction_field') and K == R.fraction_field:
                h1 = True
            elif hasattr(R, 'is_domain'):
                h1 = bool(R.is_domain)
            else:
                h1 = True
        else:
            if hasattr(R, 'is_domain'):
                h1 = bool(R.is_domain)
            elif hasattr(R, 'is_integral_domain'):
                h1 = bool(R.is_integral_domain)
            else:
                h1 = True
    except Exception:
        h1 = False

    # ¬Q: The intersection of the localized rings R_M for all maximal ideals M of R, 
    # taken as subrings of K, is NOT equal to R.
    # Mathematically, R = \bigcap R_M is unconditionally true for all commutative 
    # integral domains with a multiplicative identity (1). The conclusion fails 
    # if R is an integral domain without 1, or if R is non-commutative.
    neg_q = False
    try:
        if hasattr(R, 'intersection_of_localizations'):
            neg_q = bool(R.intersection_of_localizations() != R)
        elif hasattr(R, 'localizations_intersection'):
            neg_q = bool(R.localizations_intersection() != R)
        else:
            has_1 = True
            if hasattr(R, 'has_identity'):
                has_1 = bool(R.has_identity)
            elif hasattr(R, 'one'):
                has_1 = (R.one is not None)
            
            is_comm = True
            if hasattr(R, 'is_commutative'):
                is_comm = bool(R.is_commutative)
                
            neg_q = not (has_1 and is_comm)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "¬Q: The intersection of the localized rings R_M for all maximal ideals M of R is not equal to R"
]

N_HYP = 1
NEG_Q_INDEX = 1