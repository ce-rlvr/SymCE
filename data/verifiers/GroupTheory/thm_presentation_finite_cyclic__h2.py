import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.free_groups import free_group, FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

F, x = free_group('x')
Z_inf = F
Z = sympy.S.Integers

def is_cyclic(G):
    if G == sympy.S.Integers:
        return True
    if hasattr(G, 'is_cyclic'):
        try:
            res = G.is_cyclic
            if res is not None:
                return bool(res)
        except Exception:
            pass
    if isinstance(G, PermutationGroup):
        try:
            if G.order() == 1:
                return True
            for g in G.elements:
                if g.order() == G.order():
                    return True
        except Exception:
            pass
    if hasattr(G, 'generators'):
        try:
            if len(G.generators) <= 1:
                return True
        except Exception:
            pass
    return False

def is_finite(G):
    if G == sympy.S.Integers:
        return False
    if hasattr(G, 'is_finite'):
        try:
            res = G.is_finite
            if res is not None:
                return bool(res)
        except Exception:
            pass
    if isinstance(G, PermutationGroup):
        return True
    if isinstance(G, FreeGroup):
        try:
            return len(G.generators) == 0
        except Exception:
            pass
    if isinstance(G, FpGroup):
        try:
            from sympy import oo
            return G.order() < oo
        except Exception:
            pass
    if hasattr(G, 'order'):
        try:
            from sympy import oo
            if callable(G.order):
                return G.order() < oo
            else:
                return G.order < oo
        except Exception:
            pass
    return False

def conditions(witness):
    try:
        h1 = is_cyclic(witness)
    except Exception:
        h1 = False

    try:
        # The conclusion states G is isomorphic to <x | x^n = 1>.
        # This presentation defines a finite cyclic group.
        # Therefore, the conclusion holds iff G is a finite cyclic group.
        q = is_cyclic(witness) and is_finite(witness)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: G is not isomorphic to <x | x^n = 1> for any n >= 1 (i.e. G is not a finite cyclic group)"
]

N_HYP = 1
NEG_Q_INDEX = 1