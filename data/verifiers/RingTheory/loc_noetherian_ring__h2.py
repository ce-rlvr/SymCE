import sympy
from sympy import *

class Ring:
    def __init__(self, is_commutative=True, is_noetherian=True):
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian

class Subset:
    def __init__(self, is_mult_closed=True, elements=None):
        self.is_mult_closed = is_mult_closed
        self.elements = set(elements) if elements is not None else {1}

class LocalizedRing:
    def __init__(self, R, S):
        self.R = R
        self.S = S
        
    @property
    def is_noetherian(self):
        if self.S.elements == {1}:
            return self.R.is_noetherian
        if 0 in self.S.elements:
            return True
        raise ValueError("Cannot determine Noetherian property for arbitrary subset")

# Predefined objects for the witness
R_non_noetherian = Ring(is_commutative=True, is_noetherian=False)
S_trivial = Subset(is_mult_closed=True, elements={1})

def conditions(witness) -> list[bool]:
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = bool(R.is_commutative)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = bool(S.is_mult_closed)
    except Exception:
        h2_ok = False
        
    try:
        loc_ring = LocalizedRing(R, S)
        neg_Q_ok = not bool(loc_ring.is_noetherian)
    except Exception:
        neg_Q_ok = False
        
    return [h1_ok, h2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2