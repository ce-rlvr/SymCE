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

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: f: X -> Y is a morphism of varieties",
    "H_3: C is a constructible set in X",
    "¬Q: f(C) is not a constructible set in Y"
]

N_HYP = 3
NEG_Q_INDEX = 3

def _get_bool(witness, keys, default=False):
    """Helper to extract boolean properties from a dictionary or object."""
    if isinstance(witness, dict):
        for k in keys:
            if k in witness:
                return bool(witness[k])
    else:
        for k in keys:
            if hasattr(witness, k):
                val = getattr(witness, k)
                if callable(val):
                    return bool(val())
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    # H_1: K is an algebraically closed field
    try:
        h1 = _get_bool(witness, [
            'K_is_algebraically_closed', 
            'is_algebraically_closed', 
            'algebraically_closed'
        ], False)
    except Exception:
        h1 = False

    # H_2: f: X -> Y is a morphism of varieties
    try:
        h2 = _get_bool(witness, [
            'f_is_morphism_of_varieties', 
            'is_morphism_of_varieties', 
            'is_morphism'
        ], False)
    except Exception:
        h2 = False

    # H_3: C is a constructible set in X
    try:
        h3 = _get_bool(witness, [
            'C_is_constructible_in_X', 
            'C_is_constructible', 
            'is_constructible_in_X', 
            'domain_constructible'
        ], False)
    except Exception:
        h3 = False

    # ¬Q: f(C) is a constructible set in Y (must FAIL, so we negate it)
    try:
        q = _get_bool(witness, [
            'f_C_is_constructible_in_Y', 
            'f_C_is_constructible', 
            'is_constructible_in_Y', 
            'image_constructible'
        ], True)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]