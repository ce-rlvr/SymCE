import sympy
from sympy.ntheory import isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness represents the field F (or its characteristic).
    """
    try:
        # If witness is an integer, treat it as the characteristic of the field
        if isinstance(witness, int) or getattr(witness, 'is_Integer', False):
            val = int(witness)
            is_field = (val == 0 or isprime(val))
            char = val
        else:
            # If witness is a polynomial ring, extract its base domain
            domain = witness
            if hasattr(witness, 'domain'):
                domain = witness.domain
                
            is_field = getattr(domain, 'is_Field', False)
                
            char = None
            if hasattr(domain, 'characteristic'):
                c = domain.characteristic
                char = c() if callable(c) else c
            elif hasattr(domain, 'char'):
                c = domain.char
                char = c() if callable(c) else c
            elif hasattr(domain, 'p'):
                char = domain.p
    except Exception:
        is_field = False
        char = None

    try:
        h1 = bool(is_field)
    except Exception:
        h1 = False

    try:
        # The curve y^2 = x^3 + 1 is singular iff the characteristic is 2 or 3.
        # If it is singular, the coordinate ring is not integrally closed.
        neg_q = char in (2, 3)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: the factor ring is not an integrally closed domain"
]

N_HYP = 1
NEG_Q_INDEX = 1