import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for Ring/Field domain
# Abstract ring properties are typically evaluated via object attributes or dictionary keys.

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    """
    def get_prop(w, prop_names, default):
        if isinstance(w, dict):
            for p in prop_names:
                if p in w:
                    return bool(w[p])
            return default
        else:
            for p in prop_names:
                if hasattr(w, p):
                    val = getattr(w, p)
                    return bool(val() if callable(val) else val)
            return default

    # H_1: R is a Noetherian ring
    try:
        h1_ok = get_prop(witness, ['is_noetherian', 'is_Noetherian', 'noetherian'], False)
    except Exception:
        h1_ok = False

    # H_2: R is a local ring with maximal ideal m
    try:
        h2_ok = get_prop(witness, ['is_local', 'is_Local', 'local'], False)
    except Exception:
        h2_ok = False

    # ¬Q: The intersection of m^n for all positive integers n is NOT the zero ideal
    try:
        # If the intersection is zero, the conclusion holds (Q is True).
        # We want the negation of the conclusion (neg_Q is True when intersection is NOT zero).
        q_ok = get_prop(witness, [
            'intersection_is_zero', 
            'krull_intersection_is_zero', 
            'intersection_of_powers_is_zero'
        ], True)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: R is a local ring with maximal ideal m",
    "¬Q: The intersection of m^n for all positive integers n is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2