import sympy
import math
import itertools
import functools

class Space:
    def __init__(self, locally_compact, compact, metric, separable):
        self.locally_compact = locally_compact
        self.compact = compact
        self.metric = metric
        self.separable = separable

# Predefined spaces that might be used as witnesses
uncountable_discrete = Space(locally_compact=True, compact=False, metric=True, separable=False)
R = Space(locally_compact=True, compact=False, metric=True, separable=True)
Q = Space(locally_compact=False, compact=False, metric=True, separable=True)
Z = Space(locally_compact=True, compact=False, metric=True, separable=True)
compact_interval = Space(locally_compact=True, compact=True, metric=True, separable=True)

known_spaces = {
    "uncountable_discrete": uncountable_discrete,
    "R": R,
    "Q": Q,
    "Z": Z,
    "compact_interval": compact_interval
}

def conditions(witness) -> list[bool]:
    # Allow witness to be a string name of a known space
    if isinstance(witness, str):
        witness = known_spaces.get(witness, None)
        
    try:
        if isinstance(witness, dict):
            is_lc = bool(witness.get("locally_compact", False))
            is_c = bool(witness.get("compact", False))
            is_m = bool(witness.get("metric", False))
        else:
            is_lc = bool(witness.locally_compact)
            is_c = bool(witness.compact)
            is_m = bool(witness.metric)
        h1 = is_lc and not is_c and is_m
    except Exception:
        h1 = False
        
    try:
        if isinstance(witness, dict):
            is_sep = bool(witness.get("separable", False))
        else:
            is_sep = bool(witness.separable)
            
        # The one-point compactification of a locally compact Hausdorff space is metrizable 
        # iff the space is second-countable. For a metric space, second-countable is 
        # equivalent to separable. Thus, X* is not metrizable iff X is not separable.
        neg_q = not is_sep
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a locally compact, non-compact metric space",
    "¬Q: The one-point compactification X* is not metrizable"
]

N_HYP = 1
NEG_Q_INDEX = 1