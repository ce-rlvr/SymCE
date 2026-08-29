import sympy
from sympy import QQ, ZZ, Symbol
from sympy.polys.domains import Domain
from sympy.ntheory import factorint, isprime

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

class FormalPowerSeriesRing:
    """Represents a formal power series ring R[[x]]."""
    def __init__(self, base_ring, generator):
        self.base_ring = base_ring
        self.generator = generator
    def is_commutative(self): return True
    def is_local(self): return True
    def is_reduced(self): return True
    def is_field(self): return False

class LocalizedRing:
    """Represents a localization of a ring at a prime ideal."""
    def __init__(self, base_ring, prime):
        self.base_ring = base_ring
        self.prime = prime
    def is_commutative(self): return True
    def is_local(self): return True
    def is_reduced(self): return True
    def is_field(self): return False

class PAdicIntegers:
    """Represents the ring of p-adic integers Z_p."""
    def __init__(self, p):
        self.p = p
    def is_commutative(self): return True
    def is_local(self): return True
    def is_reduced(self): return True
    def is_field(self): return False

# Standard instances for quick access
Z_2 = PAdicIntegers(2)
Z_3 = PAdicIntegers(3)
Z_5 = PAdicIntegers(5)

def check_commutative(w):
    if isinstance(w, int):
        return w > 1
    if hasattr(w, 'is_commutative'):
        return w.is_commutative() if callable(w.is_commutative) else w.is_commutative
    if hasattr(w, 'is_Commutative'):
        return w.is_Commutative() if callable(w.is_Commutative) else w.is_Commutative
    if isinstance(w, Domain):
        return True
    return False

def check_local(w):
    if isinstance(w, int):
        if w <= 1: return False
        return len(factorint(w)) == 1
    if hasattr(w, 'is_local'):
        return w.is_local() if callable(w.is_local) else w.is_local
    if isinstance(w, Domain):
        return w.is_Field
    return False

def check_reduced(w):
    if isinstance(w, int):
        if w <= 1: return False
        return all(v == 1 for v in factorint(w).values())
    if hasattr(w, 'is_reduced'):
        return w.is_reduced() if callable(w.is_reduced) else w.is_reduced
    if isinstance(w, Domain):
        return True
    return False

def check_field(w):
    if isinstance(w, int):
        if w <= 1: return False
        return isprime(w)
    if hasattr(w, 'is_field'):
        return w.is_field() if callable(w.is_field) else w.is_field
    if hasattr(w, 'is_Field'):
        return w.is_Field() if callable(w.is_Field) else w.is_Field
    if isinstance(w, Domain):
        return w.is_Field
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(check_commutative(witness))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_local(witness))
    except Exception:
        h2 = False

    try:
        h3 = bool(check_reduced(witness))
    except Exception:
        h3 = False

    try:
        is_f = bool(check_field(witness))
        neg_q = not is_f
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring",
    "H_3: R is a reduced ring",
    "¬Q: R is not a field"
]

N_HYP = 3
NEG_Q_INDEX = 3