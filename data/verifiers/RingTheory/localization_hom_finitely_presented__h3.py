import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy does not have a module theory or localization implementation,
    the witness is expected to be a mock object (dictionary or object with attributes)
    or a list/tuple of booleans.
    """
    # If witness is a list or tuple of booleans: [H1, H2, H3, Q]
    if isinstance(witness, (list, tuple)) and len(witness) >= 4:
        try:
            return [bool(witness[0]), bool(witness[1]), bool(witness[2]), not bool(witness[3])]
        except Exception:
            pass

    def check(attrs, default=False):
        if isinstance(witness, dict):
            for attr in attrs:
                if attr in witness:
                    return bool(witness[attr])
        else:
            for attr in attrs:
                if hasattr(witness, attr):
                    return bool(getattr(witness, attr))
        return default

    try:
        h1 = check([
            'R_is_commutative_ring_with_identity', 
            'is_commutative_ring_with_identity', 
            'R_commutative'
        ], False)
    except Exception:
        h1 = False

    try:
        h2 = check([
            'M_is_finitely_presented_R_module', 
            'M_is_finitely_presented', 
            'is_finitely_presented'
        ], False)
    except Exception:
        h2 = False

    try:
        h3 = check([
            'S_is_multiplicatively_closed_subset', 
            'S_is_multiplicatively_closed', 
            'is_multiplicatively_closed'
        ], False)
    except Exception:
        h3 = False

    try:
        q = check([
            'canonical_homomorphism_is_isomorphism', 
            'is_isomorphism', 
            'homomorphism_is_isomorphism'
        ], True)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is a finitely presented R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: The canonical S^{-1}R-module homomorphism is not an isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3