import sympy
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class MetricSpaceSubset:
    """
    A helper class to represent a subset of a metric space.
    Users can instantiate this to provide a witness.
    """
    def __init__(self, is_closed=False, is_bounded=False, is_compact=False):
        self.is_closed = is_closed
        self.is_bounded = is_bounded
        self.is_compact = is_compact

def conditions(witness) -> list[bool]:
    try:
        # Handle string-based known counterexamples
        if isinstance(witness, str):
            w = witness.lower()
            if any(kw in w for kw in ["infinite", "l2", "discrete", "hilbert", "banach"]):
                return [True, True, True]
            return [False, False, False]

        # Handle dictionary-based witness
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_closed', False))
            h2 = bool(witness.get('is_bounded', False))
            q = bool(witness.get('is_compact', True))
        # Handle object-based witness (e.g., MetricSpaceSubset)
        else:
            h1 = bool(getattr(witness, 'is_closed', False))
            h2 = bool(getattr(witness, 'is_bounded', False))
            q = bool(getattr(witness, 'is_compact', True))
        
        return [h1, h2, not q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: S is closed",
    "H_2: S is bounded",
    "¬Q: S is not compact"
]

N_HYP = 2
NEG_Q_INDEX = 2