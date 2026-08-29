import sympy
from sympy import S
from sympy.abc import x, y, z

# Top-level setup
class _InfiniteBooleanRing:
    @property
    def is_Boolean_ring(self):
        return True
    
    @property
    def is_finite(self):
        return False
        
    @property
    def is_infinite(self):
        return True

class _FiniteBooleanRing:
    @property
    def is_Boolean_ring(self):
        return True
        
    @property
    def is_finite(self):
        return True
        
    @property
    def is_infinite(self):
        return False

InfiniteBooleanRing = _InfiniteBooleanRing()
FiniteBooleanRing = _FiniteBooleanRing()

def conditions(witness) -> list[bool]:
    # H_1: R is a Boolean ring
    try:
        if hasattr(witness, 'is_Boolean_ring'):
            h1 = bool(witness.is_Boolean_ring)
        elif hasattr(witness, 'is_boolean_ring'):
            h1 = bool(witness.is_boolean_ring)
        elif type(witness).__name__ == 'PowerSet':
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: R is not a finite ring
    try:
        if hasattr(witness, 'is_finite'):
            neg_q = not bool(witness.is_finite)
        elif hasattr(witness, 'is_infinite'):
            neg_q = bool(witness.is_infinite)
        elif type(witness).__name__ == 'PowerSet':
            neg_q = not bool(witness.base.is_finite)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1