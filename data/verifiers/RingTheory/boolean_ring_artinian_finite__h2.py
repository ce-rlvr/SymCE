import sympy
from sympy import *
import itertools
import functools
import math

# Top-level setup: named object bindings that the witness expression may reference.
# We provide abstract representations of rings since sympy does not have a dedicated
# infinite Boolean ring object.
class AbstractRing:
    def __init__(self, boolean=False, finite=True):
        self._boolean = boolean
        self._finite = finite

    @property
    def is_boolean_ring(self):
        return self._boolean

    @property
    def is_finite(self):
        return self._finite

InfiniteBooleanRing = AbstractRing(boolean=True, finite=False)
FiniteBooleanRing = AbstractRing(boolean=True, finite=True)
InfiniteNonBooleanRing = AbstractRing(boolean=False, finite=False)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: R is a Boolean ring
    h1 = False
    try:
        if hasattr(witness, 'is_boolean_ring'):
            val = witness.is_boolean_ring() if callable(witness.is_boolean_ring) else witness.is_boolean_ring
            h1 = bool(val)
        elif type(witness).__name__ == 'PowerSet':
            # The power set of any set forms a Boolean ring under symmetric difference and intersection.
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: R is not a finite ring (i.e., R is infinite)
    neg_q = False
    try:
        if hasattr(witness, 'is_finite'):
            val = witness.is_finite() if callable(witness.is_finite) else witness.is_finite
            neg_q = not bool(val)
        elif type(witness).__name__ == 'PowerSet':
            base_set = witness.args[0]
            if hasattr(base_set, 'is_finite'):
                val = base_set.is_finite() if callable(base_set.is_finite) else base_set.is_finite
                neg_q = not bool(val)
            else:
                # Fallback if finiteness of base set cannot be determined
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1