import sympy
from sympy import Interval, S
import math
import itertools
import functools

class TopologicalSpace:
    def __init__(self, name, is_pseudocompact, is_compact, is_metrizable):
        self.name = name
        self.is_pseudocompact = is_pseudocompact
        self.is_compact = is_compact
        self.is_metrizable = is_metrizable

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Known topological spaces for testing
omega_1 = TopologicalSpace("omega_1", True, False, False)
Tychonoff_plank = TopologicalSpace("Tychonoff_plank", True, False, False)
beta_N = TopologicalSpace("beta_N", True, True, False)
R = TopologicalSpace("R", False, False, True)
compact_interval = TopologicalSpace("[0, 1]", True, True, True)
N = TopologicalSpace("N", False, False, True)
Sorgenfrey_line = TopologicalSpace("Sorgenfrey_line", False, False, False)
Q = TopologicalSpace("Q", False, False, True)

def conditions(witness) -> list[bool]:
    if isinstance(witness, str):
        witness_obj = globals().get(witness, None)
        if witness_obj is None:
            for obj in globals().values():
                if isinstance(obj, TopologicalSpace) and obj.name == witness:
                    witness_obj = obj
                    break
        witness = witness_obj

    if hasattr(witness, 'is_subset') and hasattr(witness, 'is_closed'):
        try:
            if witness.is_subset(sympy.S.Reals):
                is_bounded = witness.inf.is_finite and witness.sup.is_finite
                is_compact = witness.is_closed and is_bounded
                h1 = bool(is_compact)
                neg_q = not bool(is_compact)
                return [h1, neg_q]
        except Exception:
            pass

    try:
        h1 = bool(witness.is_pseudocompact)
    except Exception:
        h1 = False

    try:
        neg_q = not bool(witness.is_compact and witness.is_metrizable)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Every continuous function f: X -> R is bounded",
    "¬Q: X is not a compact metric space"
]

N_HYP = 1
NEG_Q_INDEX = 1