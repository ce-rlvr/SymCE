import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _get_group(g_cand):
    if isinstance(g_cand, Permutation):
        return PermutationGroup([g_cand])
    elif isinstance(g_cand, list) and len(g_cand) > 0 and all(isinstance(p, Permutation) for p in g_cand):
        return PermutationGroup(g_cand)
    elif isinstance(g_cand, PermutationGroup):
        return g_cand
    return None

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        G = None
        degree = None
        
        # Witness can be a tuple (Group, Set_Size) or just a Group (where Set_Size = Group.degree)
        if isinstance(witness, tuple) and len(witness) == 2:
            g_cand, x_cand = witness
            G = _get_group(g_cand)
            if G is not None:
                if isinstance(x_cand, int) and x_cand >= G.degree:
                    degree = x_cand
                    h1 = True
                    h2 = True
                elif isinstance(x_cand, (list, set, tuple)) and len(x_cand) >= G.degree:
                    degree = len(x_cand)
                    h1 = True
                    h2 = True
        else:
            G = _get_group(witness)
            if G is not None:
                degree = G.degree
                h1 = True
                h2 = True
                
    except Exception:
        pass

    try:
        if h1 and h2 and G is not None and degree is not None:
            # By Burnside's Lemma, sum_{g in G} |X^g| = |orbits| * |G|
            # So the sum equals |G| if and only if the number of orbits is exactly 1.
            # The number of orbits is the orbits within the group's degree plus any extra fixed points.
            orbits_count = len(G.orbits()) + (degree - G.degree)
            neg_q = bool(orbits_count != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set",
    "¬Q: sum_{g in G} |X^g| != |G|"
]

N_HYP = 2
NEG_Q_INDEX = 2