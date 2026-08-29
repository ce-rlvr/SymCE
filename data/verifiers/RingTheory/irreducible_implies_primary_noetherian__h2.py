import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

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

def _check_prop(witness, prop_names, default=False):
    """
    Helper to check for properties or methods on the witness object or dictionary.
    """
    if isinstance(witness, dict):
        for name in prop_names:
            if name in witness:
                val = witness[name]
                return bool(val() if callable(val) else val)
    
    for name in prop_names:
        if hasattr(witness, name):
            try:
                val = getattr(witness, name)
                return bool(val() if callable(val) else val)
            except Exception:
                pass
                
    if isinstance(witness, (list, tuple)):
        for item in witness:
            for name in prop_names:
                if hasattr(item, name):
                    try:
                        val = getattr(item, name)
                        return bool(val() if callable(val) else val)
                    except Exception:
                        pass
                        
    return default

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring with identity
    try:
        h1 = _check_prop(witness, ['is_commutative_ring_with_identity', 'is_commutative_ring', 'is_ring'])
    except Exception:
        h1 = False

    # H_2: I is a proper ideal of R
    try:
        h2 = _check_prop(witness, ['is_proper_ideal', 'is_proper'])
    except Exception:
        h2 = False

    # H_3: I is an irreducible ideal
    try:
        h3 = _check_prop(witness, ['is_irreducible_ideal', 'is_irreducible'])
    except Exception:
        h3 = False

    # ¬Q: I is not a primary ideal
    try:
        q = _check_prop(witness, ['is_primary_ideal', 'is_primary'], default=None)
        if q is None:
            neg_q = False
        else:
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "H_3: I is an irreducible ideal",
    "¬Q: I is not a primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3