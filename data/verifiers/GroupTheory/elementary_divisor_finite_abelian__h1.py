import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.abc
import sympy.polys
import sympy.ntheory
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

def check_group(G):
    from sympy import S
    if G in (S.Integers, S.Reals, S.Rationals, S.Complexes):
        return True
    if G in (S.Naturals, S.Naturals0):
        return False
    if type(G).__name__ in ('FreeGroup', 'FpGroup', 'PermutationGroup', 'ProductGroup'):
        return True
    if hasattr(G, 'is_group'):
        val = G.is_group
        if callable(val):
            return bool(val())
        return bool(val)
    if hasattr(G, 'identity') and hasattr(G, 'generators'):
        return True
    return False

def check_abelian(G):
    if not check_group(G):
        return False
    from sympy import S
    if G in (S.Integers, S.Reals, S.Rationals, S.Complexes):
        return True
    if type(G).__name__ == 'FreeGroup':
        return len(G.generators) <= 1
    try:
        if hasattr(G, 'is_abelian'):
            val = G.is_abelian
            if callable(val):
                return bool(val())
            return bool(val)
    except Exception:
        pass
    return False

def check_finite(G):
    from sympy import S, oo
    if G in (S.Integers, S.Reals, S.Rationals, S.Complexes):
        return False
    if type(G).__name__ == 'FreeGroup':
        return len(G.generators) == 0
    try:
        if hasattr(G, 'order'):
            val = G.order
            if callable(val):
                val = val()
            return val != oo
    except Exception:
        pass
    try:
        if hasattr(G, 'is_finite'):
            val = G.is_finite
            if callable(val):
                return bool(val())
            return bool(val)
    except Exception:
        pass
    if type(G).__name__ == 'PermutationGroup' or hasattr(G, 'elements'):
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = check_abelian(witness)
    except Exception:
        h1 = False

    try:
        is_fin = check_finite(witness)
        is_ab = check_abelian(witness)
        
        # The conclusion states that G is isomorphic to a direct product of cyclic groups 
        # of prime-power orders, and this decomposition is unique.
        # By the Fundamental Theorem of Finite Abelian Groups, this is true IF AND ONLY IF 
        # G is a finite abelian group.
        # For infinite abelian groups (like Z) or non-abelian groups, the conclusion fails.
        conclusion = is_fin and is_ab
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: G is not isomorphic to a direct product of cyclic groups of prime-power orders (or decomposition is not unique)"
]

N_HYP = 1
NEG_Q_INDEX = 1