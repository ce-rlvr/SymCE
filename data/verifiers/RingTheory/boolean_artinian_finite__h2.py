import sympy
import math
import itertools
import functools

class InfiniteBooleanRing:
    """An infinite Boolean ring (e.g., the ring of finite and cofinite subsets of N)."""
    @property
    def is_boolean_ring(self):
        return True
    
    @property
    def is_finite(self):
        return False
        
    @property
    def is_ring(self):
        return True

class FiniteBooleanRing:
    """A finite Boolean ring."""
    def __init__(self, size=2):
        self.size = size

    @property
    def is_boolean_ring(self):
        return True
        
    @property
    def is_finite(self):
        return True
        
    @property
    def is_ring(self):
        return True
        
    def __len__(self):
        return self.size

def conditions(witness):
    try:
        if hasattr(witness, 'is_boolean_ring'):
            val = getattr(witness, 'is_boolean_ring')
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_boolean'):
            val = getattr(witness, 'is_boolean')
            h1 = bool(val() if callable(val) else val)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_finite'):
            val = getattr(witness, 'is_finite')
            is_fin = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_Finite'):
            val = getattr(witness, 'is_Finite')
            is_fin = bool(val() if callable(val) else val)
        else:
            try:
                len(witness)
                is_fin = True
            except Exception:
                is_fin = False
        neg_q = not is_fin
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1