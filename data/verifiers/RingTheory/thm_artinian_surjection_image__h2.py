import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.polys.domains.domain import Domain
from sympy import S

# Top-level setup: named object bindings that the witness expression may reference.
class CustomRing:
    def __init__(self, name, artinian):
        self.name = name
        self.artinian = artinian

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Define common rings that might be used as witnesses
Z = CustomRing("Z", False)
Q = CustomRing("Q", True)
R_ring = CustomRing("R", True)
C_ring = CustomRing("C", True)
Z2 = CustomRing("Z2", True)
Z3 = CustomRing("Z3", True)
Z4 = CustomRing("Z4", True)
Z6 = CustomRing("Z6", True)
Qx = CustomRing("Qx", False)
Zx = CustomRing("Zx", False)

def is_ring(obj):
    if isinstance(obj, CustomRing):
        return True
    if isinstance(obj, Domain):
        return True
    if obj in (S.Integers, S.Reals, S.Complexes, S.Rationals):
        return True
    return False

def is_artinian(obj):
    if isinstance(obj, CustomRing):
        return obj.artinian
    if isinstance(obj, Domain):
        if getattr(obj, 'is_Field', False):
            return True
        if obj == ZZ:
            return False
        if getattr(obj, 'is_PolynomialRing', False):
            return False
    if obj in (S.Reals, S.Complexes, S.Rationals):
        return True
    if obj == S.Integers:
        return False
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, S), check if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        R_obj, S_obj = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R and S are rings
    try:
        h1_ok = bool(is_ring(R_obj) and is_ring(S_obj))
    except Exception:
        h1_ok = False
        
    # H_2: R is an Artinian ring
    try:
        h2_ok = bool(is_artinian(R_obj))
    except Exception:
        h2_ok = False
        
    # ¬Q: S is not an Artinian ring
    try:
        neg_q_ok = not bool(is_artinian(S_obj))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: R is an Artinian ring",
    "¬Q: S is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2