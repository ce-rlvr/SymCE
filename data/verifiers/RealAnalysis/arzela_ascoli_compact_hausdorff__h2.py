import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# (No specific named objects needed for this Real Analysis theorem)

def _check_prop(witness, keys, default):
    if isinstance(witness, dict):
        for k in keys:
            if k in witness:
                return bool(witness[k])
    for k in keys:
        if hasattr(witness, k):
            try:
                val = getattr(witness, k)
                if callable(val):
                    return bool(val())
                return bool(val)
            except Exception:
                pass
    return default

def conditions(witness) -> list[bool]:
    try:
        h1 = _check_prop(witness, ["X_compact_hausdorff", "is_compact_hausdorff", "compact_hausdorff"], False)
    except Exception:
        h1 = False

    try:
        h2 = _check_prop(witness, ["F_pointwise_bounded", "is_pointwise_bounded", "pointwise_bounded"], False)
    except Exception:
        h2 = False

    try:
        h3 = _check_prop(witness, ["F_equicontinuous", "is_equicontinuous", "equicontinuous"], False)
    except Exception:
        h3 = False

    try:
        q = _check_prop(witness, ["F_closure_compact", "is_closure_compact", "closure_compact"], True)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact Hausdorff space",
    "H_2: The family F is pointwise bounded",
    "H_3: The family F is equicontinuous",
    "¬Q: The closure of F in the uniform topology is not compact"
]

N_HYP = 3
NEG_Q_INDEX = 3