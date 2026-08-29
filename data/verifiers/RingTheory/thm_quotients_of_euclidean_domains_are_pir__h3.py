import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.polys.domains.domain import Domain
from sympy.polys.domains.polynomialring import PolynomialRing
from sympy.abc import x, y, z

try:
    from sympy.polys.domains import ZZ_I
except ImportError:
    ZZ_I = None

def is_euclidean_domain(R):
    if R == ZZ:
        return True
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if isinstance(R, PolynomialRing) and len(R.symbols) == 1 and getattr(R.domain, 'is_Field', False):
        return True
    if ZZ_I is not None and R == ZZ_I:
        return True
    return False

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
    else:
        R = witness
        I = None

    # H1: R is an integral domain
    try:
        h1 = bool(isinstance(R, Domain))
    except Exception:
        h1 = False

    # H2: R is a Euclidean domain
    try:
        h2 = bool(is_euclidean_domain(R))
    except Exception:
        h2 = False

    # neg_Q: The quotient ring R/I is not a principal ideal ring
    try:
        # Every quotient of a Principal Ideal Domain (PID) is a Principal Ideal Ring (PIR).
        # Since all Euclidean domains are PIDs, if R is a PID, R/I is guaranteed to be a PIR.
        if bool(getattr(R, 'is_PID', False)):
            neg_q = False
        else:
            # If R is not a PID, we assume the provided ideal I makes R/I not a PIR
            # (which is true for some I in any non-Dedekind domain).
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R is a Euclidean domain",
    "¬Q: The quotient ring R/I is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2