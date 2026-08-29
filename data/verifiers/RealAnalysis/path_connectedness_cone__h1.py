import sympy
import math
import itertools
import functools

# Top-level setup
EmptySet = sympy.EmptySet

def conditions(witness):
    try:
        # The hypothesis establishes the definition of the cone CX over X.
        # This is structurally true for any topological space X.
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # The conclusion states that CX is path-connected.
        # The cone over any non-empty space is path-connected (all points connect to the vertex).
        # However, the cone over the empty set is the empty set, which is NOT path-connected.
        # Therefore, the conclusion fails (neg_Q is True) if and only if the witness is the empty set.
        is_empty = False
        if witness is None:
            is_empty = True
        elif witness is sympy.EmptySet or witness is sympy.S.EmptySet:
            is_empty = True
        elif isinstance(witness, (set, list, tuple)) and len(witness) == 0:
            is_empty = True
        elif isinstance(witness, str) and witness.lower().replace(" ", "") in ["empty", "emptyset", "none"]:
            is_empty = True
            
        neg_q = is_empty
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: CX is the cone over X",
    "¬Q: CX is not path-connected"
]

N_HYP = 1
NEG_Q_INDEX = 1