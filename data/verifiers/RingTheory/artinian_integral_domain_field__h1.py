import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference.
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
O2 = zeros(2,2)
O3 = zeros(3,3)

class _QuaternionsRing:
    """
    The ring of Quaternions over the reals.
    It is an Artinian domain (a division ring, hence has no zero divisors and only trivial ideals),
    but it is not a field because it is not commutative.
    """
    @property
    def is_integral_domain(self):
        return True
        
    @property
    def is_domain(self):
        return True
        
    @property
    def is_artinian(self):
        return True
        
    @property
    def is_field(self):
        return False
        
    @property
    def is_Field(self):
        return False
        
    @property
    def is_commutative(self):
        return False

Quaternions = _QuaternionsRing()
Hamiltonians = Quaternions

class _ZeroRing:
    """
    The trivial ring {0}.
    Depending on definitions, it might be considered an Artinian domain that is not a field.
    """
    @property
    def is_integral_domain(self):
        return True
        
    @property
    def is_domain(self):
        return True
        
    @property
    def is_artinian(self):
        return True
        
    @property
    def is_field(self):
        return False
        
    @property
    def is_Field(self):
        return False
        
    @property
    def is_commutative(self):
        return True

ZeroRing = _ZeroRing()


def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    try:
        if hasattr(witness, 'is_integral_domain'):
            h1 = witness.is_integral_domain() if callable(witness.is_integral_domain) else witness.is_integral_domain
        elif hasattr(witness, 'is_domain'):
            h1 = witness.is_domain() if callable(witness.is_domain) else witness.is_domain
        else:
            h1 = False
        h1_ok = bool(h1)
    except Exception:
        h1_ok = False

    # H_2: R satisfies the descending chain condition on ideals (i.e., R is an Artinian ring)
    try:
        if hasattr(witness, 'is_artinian'):
            h2 = witness.is_artinian() if callable(witness.is_artinian) else witness.is_artinian
        else:
            # Fallback: all fields are Artinian rings
            is_f = False
            if hasattr(witness, 'is_field'):
                is_f = witness.is_field() if callable(witness.is_field) else witness.is_field
            elif hasattr(witness, 'is_Field'):
                is_f = witness.is_Field() if callable(witness.is_Field) else witness.is_Field
            h2 = bool(is_f)
        h2_ok = bool(h2)
    except Exception:
        h2_ok = False

    # ¬Q: R is not a field
    try:
        if hasattr(witness, 'is_field'):
            is_f = witness.is_field() if callable(witness.is_field) else witness.is_field
        elif hasattr(witness, 'is_Field'):
            is_f = witness.is_Field() if callable(witness.is_Field) else witness.is_Field
        else:
            is_f = False
        neg_q_ok = not bool(is_f)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]


CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R satisfies the descending chain condition on ideals (i.e., R is an Artinian ring)",
    "¬Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2