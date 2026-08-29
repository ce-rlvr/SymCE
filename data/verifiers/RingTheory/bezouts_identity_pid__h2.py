import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

# Top-level setup for Ring Theory
# Standard commutative domains are available via sympy.ZZ and sympy.QQ.
# Polynomial rings can be constructed via QQ.old_poly_ring(x), etc.

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and fails the conclusion of the conjecture.
    
    The witness is expected to be a tuple (R, a, b, d) or an object with
    attributes R, a, b, d. If R is omitted in a 3-tuple, ZZ is assumed.
    """
    h1, h2, neg_q = False, False, False
    
    R, a, b, d = None, None, None, None
    if isinstance(witness, tuple):
        if len(witness) == 4:
            R, a, b, d = witness
        elif len(witness) == 3:
            a, b, d = witness
            R = ZZ
    else:
        try:
            R = witness.R
            a = witness.a
            b = witness.b
            d = witness.d
        except AttributeError:
            pass

    if R is None:
        return [False, False, False]

    # H_1: R is a principal ideal domain
    try:
        if hasattr(R, 'is_PID'):
            h1 = bool(R.is_PID)
        elif hasattr(R, 'is_principal_ideal_domain'):
            h1 = bool(R.is_principal_ideal_domain())
        else:
            # Fallback for standard SymPy domains if property is missing
            if R in (ZZ, QQ):
                h1 = True
    except Exception:
        h1 = False

    # H_2: d is a greatest common divisor of a and b
    try:
        if hasattr(R, 'is_gcd'):
            h2 = bool(R.is_gcd(a, b, d))
        elif hasattr(R, 'gcd'):
            g = R.gcd(a, b)
            if g == 0 and d == 0:
                h2 = True
            elif d == 0 or g == 0:
                h2 = False
            else:
                if hasattr(R, 'div'):
                    q1, r1 = R.div(g, d)
                    q2, r2 = R.div(d, g)
                    h2 = (r1 == 0) and (r2 == 0)
                else:
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: There do NOT exist elements x and y in R such that d = ax + by
    try:
        if hasattr(R, 'has_bezout_coefficients'):
            neg_q = not bool(R.has_bezout_coefficients(a, b, d))
        elif hasattr(R, 'gcdex'):
            # For commutative PIDs, if d is a gcd, it is an associate of g = ax + by.
            # Thus d = g*q = a(xq) + b(yq), meaning a solution always exists.
            x_coeff, y_coeff, g = R.gcdex(a, b)
            if d == 0 and g == 0:
                neg_q = False
            elif g == 0:
                neg_q = True
            else:
                if hasattr(R, 'div'):
                    q, r = R.div(d, g)
                    if r == 0:
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: d is a greatest common divisor of a and b",
    "¬Q: There do not exist elements x and y in R such that d = ax + by"
]

N_HYP = 2
NEG_Q_INDEX = 2