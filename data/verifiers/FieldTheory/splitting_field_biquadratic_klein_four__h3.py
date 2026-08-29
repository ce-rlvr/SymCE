import sympy
from sympy import Rational, sqrt, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.polys.domains import QQ

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

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: a and b are elements of F",
    "¬Q: The splitting field of (x^2 - a)(x^2 - b) over F does not have degree 4, or its Galois group is not the Klein four-group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    F = None
    if isinstance(witness, tuple):
        if len(witness) == 2:
            F = QQ
            a, b = witness
        elif len(witness) == 3:
            F, a, b = witness
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    if F == 'QQ':
        F = QQ

    # H1: F is a field of char != 2
    try:
        char = F.characteristic()
        h1 = bool((char != 2) and getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H2: a and b are elements of F
    try:
        if hasattr(F, 'convert'):
            F.convert(a)
            F.convert(b)
            h2 = True
        else:
            Rational(a)
            Rational(b)
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: degree is not 4
    try:
        if F == QQ:
            def is_sq(x):
                if x == 0: 
                    return True
                r = Rational(x)
                if r < 0: 
                    return False
                return sqrt(r).is_rational
            
            deg4 = (not is_sq(a)) and (not is_sq(b)) and (not is_sq(a * b))
            neg_q = not deg4
        elif getattr(F, 'is_FiniteField', False):
            # Over any finite field, the splitting field of a biquadratic has degree at most 2
            neg_q = True
        else:
            # Fallback for other fields: if a or b is 0, or a == b, degree is definitely not 4
            if a == b or a == 0 or b == 0:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]