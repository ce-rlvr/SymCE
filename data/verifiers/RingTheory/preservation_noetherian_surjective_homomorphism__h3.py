import sympy
from sympy import *

class Ring:
    def __init__(self, name, is_commutative, is_noetherian):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian
        
    def __eq__(self, other):
        return isinstance(other, Ring) and self.name == other.name
        
    def __hash__(self):
        return hash(self.name)
        
    def __str__(self):
        return self.name

class RingHomomorphism:
    def __init__(self, domain, codomain, is_surjective):
        self.domain = domain
        self.codomain = codomain
        self.is_surjective = is_surjective

# Top-level setup: named object bindings
# Standard Noetherian rings
Z = Ring("Z", True, True)
Q = Ring("Q", True, True)
Z_x = Ring("Z[x]", True, True)

# Standard non-Noetherian rings
Poly_inf = Ring("k[x_1, x_2, ...]", True, False)
C_R = Ring("C(R)", True, False)

# Standard non-commutative rings
FreeAlg = Ring("k<x,y>", False, True)

def id_hom(ring):
    return RingHomomorphism(ring, ring, True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            f = witness.get('f')
        else:
            R, S, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R and S are commutative rings
    try:
        h1 = getattr(R, 'is_commutative', False) and getattr(S, 'is_commutative', False)
    except Exception:
        h1 = False
        
    # H_2: f: R -> S is a surjective ring homomorphism
    try:
        h2 = (getattr(f, 'domain', None) == R) and \
             (getattr(f, 'codomain', None) == S) and \
             getattr(f, 'is_surjective', False)
    except Exception:
        h2 = False
        
    # ¬Q: S is not a Noetherian ring
    try:
        # If S is not a Ring object or lacks the attribute, we default to True (meaning it IS Noetherian, so neg_q is False)
        # We only want neg_q to be True if we are certain S is NOT Noetherian.
        is_noeth = getattr(S, 'is_noetherian', True)
        neg_q = not is_noeth
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R -> S is a surjective ring homomorphism",
    "¬Q: S is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2