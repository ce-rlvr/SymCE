import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Given a witness tuple (R, a, b, d1, d2), checks the hypotheses and the negated conclusion.
    R is expected to be a SymPy domain (e.g., ZZ, QQ, QQ.old_poly_ring(x)).
    """
    try:
        R, a, b, d1, d2 = witness
    except Exception:
        return [False, False, False, False]

    def divides(domain, divisor, dividend):
        if divisor == domain.zero:
            return dividend == domain.zero
        try:
            domain.exquo(dividend, divisor)
            return True
        except Exception:
            return False

    def is_unit(domain, u):
        return divides(domain, u, domain.one)

    # H_1: R is a unique factorization domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H_2: a and b are elements of R
    try:
        h2 = bool(a in R and b in R)
    except Exception:
        h2 = False

    # H_3: d1 is a greatest common divisor of a and b
    try:
        h3 = False
        if d1 in R and divides(R, d1, a) and divides(R, d1, b):
            g = R.gcd(a, b)
            # In a UFD, any common divisor divides the GCD.
            # If the GCD also divides d1, they are associates, making d1 a GCD.
            if divides(R, g, d1):
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: For all units u in R, d1 != u * d2
    try:
        def conclusion_holds(domain, d1, d2):
            if d2 not in domain:
                return False
            if d2 == domain.zero:
                return d1 == domain.zero
            if not divides(domain, d2, d1):
                return False
            u = domain.exquo(d1, d2)
            return is_unit(domain, u)
            
        neg_q = not conclusion_holds(R, d1, d2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a and b are elements of R",
    "H_3: d1 is a greatest common divisor of a and b",
    "¬Q: For all units u in R, d1 != u * d2"
]

N_HYP = 3
NEG_Q_INDEX = 3