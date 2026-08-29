import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import eye, zeros
import sympy.abc
import sympy.polys
import sympy.ntheory
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

def _get_prop(witness, prop_name, default=None):
    """
    Helper function to safely extract a boolean property from the witness.
    Supports dictionary keys, object attributes/methods, and SymPy Sets.
    """
    if isinstance(witness, dict) and prop_name in witness:
        return bool(witness[prop_name])
    
    if hasattr(witness, prop_name):
        val = getattr(witness, prop_name)
        if callable(val):
            try:
                return bool(val())
            except Exception:
                pass
        elif val is not None:
            return bool(val)
            
    # Fallback for SymPy Sets (for subsets of R, connected implies locally path-connected and path-connected)
    if isinstance(witness, sympy.Set):
        if witness.is_connected is not None:
            return bool(witness.is_connected)
            
    return default

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    """
    try:
        h1 = _get_prop(witness, 'is_connected', default=False)
    except Exception:
        h1 = False

    try:
        h2 = _get_prop(witness, 'is_locally_path_connected', default=False)
    except Exception:
        h2 = False

    try:
        # The conclusion Q is that X is path-connected.
        # We want neg_Q to be True if X is NOT path-connected.
        q = _get_prop(witness, 'is_path_connected', default=True)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a connected space",
    "H_2: X is a locally path-connected space",
    "¬Q: X is not a path-connected space"
]

N_HYP = 2
NEG_Q_INDEX = 2