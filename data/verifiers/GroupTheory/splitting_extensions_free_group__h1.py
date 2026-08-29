import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2) # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    # Allow witness to be a dictionary for flexibility
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_ses', False))
            h2 = bool(witness.get('is_free_group', False))
            neg_q = not bool(witness.get('splits', True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # Allow witness to be an object with attributes
    if hasattr(witness, 'is_ses'):
        try:
            h1 = bool(witness.is_ses)
            h2 = bool(witness.is_free_group)
            neg_q = not bool(witness.splits)
            return [h1, h2, neg_q]
        except Exception:
            pass

    # Otherwise, assume witness is a tuple (G, N, F)
    try:
        G = witness[0]
        N = witness[1]
        F = witness[2]
    except Exception:
        return [False, False, False]
        
    # H1: 1 -> N -> G -> F -> 1 is a short exact sequence
    try:
        if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
            if hasattr(N, 'is_normal') and N.is_normal(G):
                if hasattr(G, 'order') and hasattr(N, 'order') and hasattr(F, 'order'):
                    if G.order() == N.order() * F.order():
                        h1 = True
    except Exception:
        pass

    # H2: F is a free group
    try:
        if isinstance(F, FreeGroup):
            h2 = True
        elif hasattr(F, 'order') and F.order() == 1:
            h2 = True
    except Exception:
        pass

    # neg_Q: The sequence does NOT split
    try:
        if hasattr(G, 'subgroups'):
            splits = False
            for H in G.subgroups():
                if hasattr(H, 'order') and hasattr(F, 'order') and H.order() == F.order():
                    intersect_trivial = True
                    for g in H.elements:
                        if g != G.identity and g in N:
                            intersect_trivial = False
                            break
                    if intersect_trivial:
                        splits = True
                        break
            neg_q = not splits
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: 1 -> N -> G -> F -> 1 is a short exact sequence",
    "H_2: F is a free group",
    "¬Q: The sequence does not split (G is not a semidirect product of N and F)"
]

N_HYP = 2
NEG_Q_INDEX = 2