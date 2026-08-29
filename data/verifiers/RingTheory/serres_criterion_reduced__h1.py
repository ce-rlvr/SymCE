import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def _get_bool_prop(witness, prop_names):
    """Helper to extract boolean properties from a mock object or dictionary."""
    if isinstance(witness, dict):
        for p in prop_names:
            if p in witness:
                val = witness[p]
                if callable(val):
                    return bool(val())
                return bool(val)
    else:
        for p in prop_names:
            if hasattr(witness, p):
                val = getattr(witness, p)
                if callable(val):
                    return bool(val())
                return bool(val)
    raise ValueError(f"None of the properties {prop_names} found on witness")

def conditions(witness) -> list[bool]:
    # H_1: R satisfies Serre's condition (R0)
    try:
        h1 = _get_bool_prop(witness, ['is_R0', 'satisfies_R0', 'R0', 'r0', 'satisfies_r0'])
    except Exception:
        h1 = False

    # H_2: R satisfies Serre's condition (S1)
    try:
        h2 = _get_bool_prop(witness, ['is_S1', 'satisfies_S1', 'S1', 's1', 'satisfies_s1'])
    except Exception:
        h2 = False

    # ¬Q: R is NOT a reduced ring
    try:
        is_red = _get_bool_prop(witness, ['is_reduced', 'reduced', 'is_reduced_ring'])
        neg_q = not is_red
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R satisfies Serre's condition (R0)",
    "H_2: R satisfies Serre's condition (S1)",
    "¬Q: R is not a reduced ring"
]

N_HYP = 2
NEG_Q_INDEX = 2