import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    h1 = False
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_integral_domain', False))
        elif hasattr(witness, 'is_integral_domain'):
            val = getattr(witness, 'is_integral_domain')
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_IntegralDomain'):
            val = getattr(witness, 'is_IntegralDomain')
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_domain'):
            val = getattr(witness, 'is_domain')
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # neg_Q: The intersection of the localized rings R_M for all maximal ideals M of R, 
    # taken as subrings of K, is NOT equal to R
    neg_q = False
    try:
        if isinstance(witness, dict):
            if 'intersection_of_localizations_equals_R' in witness:
                neg_q = not bool(witness['intersection_of_localizations_equals_R'])
        elif hasattr(witness, 'intersection_of_localizations_equals_R'):
            val = getattr(witness, 'intersection_of_localizations_equals_R')
            neg_q = not bool(val() if callable(val) else val)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The intersection of the localized rings R_M for all maximal ideals M of R, taken as subrings of K, is not equal to R"
]

N_HYP = 1
NEG_Q_INDEX = 1