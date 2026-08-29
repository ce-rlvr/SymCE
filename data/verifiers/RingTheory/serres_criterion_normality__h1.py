import sympy
from sympy import symbols, Rational, Integer
import math
import itertools
import functools

# Top-level setup
x, y, z = symbols('x y z')

def check_property(witness, prop_names, default=False):
    if isinstance(witness, dict):
        for p in prop_names:
            if p in witness:
                return bool(witness[p])
    else:
        for p in prop_names:
            if hasattr(witness, p):
                val = getattr(witness, p)
                if callable(val):
                    return bool(val())
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    # H_1: R satisfies Serre's condition (R1)
    try:
        if isinstance(witness, tuple) and len(witness) >= 3:
            h1 = bool(witness[0])
        else:
            h1 = check_property(witness, ['is_R1', 'satisfies_R1', 'R1', 'r1'], False)
    except Exception:
        h1 = False

    # H_2: R satisfies Serre's condition (S2)
    try:
        if isinstance(witness, tuple) and len(witness) >= 3:
            h2 = bool(witness[1])
        else:
            h2 = check_property(witness, ['is_S2', 'satisfies_S2', 'S2', 's2'], False)
    except Exception:
        h2 = False

    # ¬Q: R is not a normal ring
    try:
        if isinstance(witness, tuple) and len(witness) >= 3:
            is_normal = bool(witness[2])
        else:
            is_normal = check_property(witness, ['is_normal', 'normal', 'is_normal_ring'], True)
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R satisfies Serre's condition (R1)",
    "H_2: R satisfies Serre's condition (S2)",
    "¬Q: R is not a normal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2