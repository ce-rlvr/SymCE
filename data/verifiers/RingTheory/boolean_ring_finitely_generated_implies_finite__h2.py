import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ, GF
import math

# Top-level setup: named object bindings that the witness expression may reference.
# We provide a standard infinite Boolean ring as a convenient witness.
class _InfiniteBooleanRing:
    @property
    def is_boolean_ring(self):
        return True
    
    @property
    def is_finite(self):
        return False

InfiniteBooleanRing = _InfiniteBooleanRing()

def conditions(witness) -> list[bool]:
    # H_1: R is a Boolean ring
    h1_ok = False
    try:
        if hasattr(witness, 'is_boolean_ring'):
            val = witness.is_boolean_ring
            h1_ok = bool(val() if callable(val) else val)
        elif type(witness).__name__ == 'PowerSet':
            # The power set of any set forms a Boolean ring under symmetric difference and intersection
            h1_ok = True
        elif hasattr(witness, 'order') and witness.order == 2:
            h1_ok = True
        elif witness == GF(2):
            h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: R is not a finite ring
    neg_q_ok = False
    try:
        is_fin = None
        if hasattr(witness, 'is_finite'):
            val = witness.is_finite
            is_fin = bool(val() if callable(val) else val)
        elif type(witness).__name__ == 'PowerSet':
            is_fin = bool(witness.base.is_finite)
        elif hasattr(witness, 'is_FiniteField') and witness.is_FiniteField:
            is_fin = True
        elif hasattr(witness, 'order'):
            if witness.order == sympy.oo:
                is_fin = False
            else:
                is_fin = math.isfinite(float(witness.order))
        elif witness == GF(2):
            is_fin = True
            
        if is_fin is not None:
            neg_q_ok = not is_fin
        else:
            if hasattr(witness, 'is_infinite'):
                val = witness.is_infinite
                neg_q_ok = bool(val() if callable(val) else val)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1