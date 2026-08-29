import sympy
from sympy import *
import math
import itertools
import functools

class _MockRing:
    def __init__(self, name, is_comm, is_local):
        self.name = name
        self.is_comm = is_comm
        self.is_loc = is_local
        
    def is_commutative(self):
        return self.is_comm
        
    def is_local(self):
        return self.is_loc
        
    def __repr__(self):
        return self.name

class _MockModule:
    def __init__(self, name, ring, is_flat, is_free):
        self.name = name
        self.ring = ring
        self._is_flat = is_flat
        self._is_free = is_free
        
    def is_flat(self, R):
        return R is self.ring and self._is_flat
        
    def is_free(self, R):
        return R is self.ring and self._is_free
        
    def __repr__(self):
        return self.name

# Predefined rings
Z = _MockRing("Z", True, False)
Z_p = _MockRing("Z_(p)", True, True)
Q = _MockRing("Q", True, True)
k_x = _MockRing("k[[x]]", True, True)
NonCommLocal = _MockRing("NonCommLocal", False, True)

# Predefined modules
Q_over_Z = _MockModule("Q", Z, True, False)
Q_over_Zp = _MockModule("Q", Z_p, True, False)
Q_over_Q = _MockModule("Q", Q, True, True)
k_x_inv = _MockModule("k((x))", k_x, True, False)
Free_Zp = _MockModule("Z_(p)^n", Z_p, True, True)
NonFlat_Zp = _MockModule("Z/pZ", Z_p, False, False)

def conditions(witness) -> list[bool]:
    try:
        R, M = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(R.is_commutative() and R.is_local())
    except Exception:
        h1 = False
        
    try:
        h2 = bool(M.is_flat(R))
    except Exception:
        h2 = False
        
    try:
        neg_q = not bool(M.is_free(R))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring",
    "H_2: M is a flat R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2