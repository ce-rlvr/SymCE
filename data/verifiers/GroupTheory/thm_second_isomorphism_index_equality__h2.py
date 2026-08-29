import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = getattr(G, 'is_group', False) or isinstance(G, sympy.combinatorics.PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        is_sub = False
        if hasattr(N, 'is_subgroup'):
            is_sub = N.is_subgroup(G)
        else:
            is_sub = all(G.contains(g) for g in N.generators)
            
        is_norm = False
        if is_sub:
            if hasattr(N, 'is_normal'):
                is_norm = N.is_normal(G)
            else:
                is_norm = all(N.contains(g * n * ~g) for n in N.generators for g in G.generators)
                
        h2 = bool(is_sub and is_norm)
    except Exception:
        h2 = False
        
    # H3: The index of H cap N in H is finite
    try:
        if hasattr(H, 'intersect'):
            H_cap_N = H.intersect(N)
        else:
            H_cap_N = H.intersection(N)
        idx = H.order() // H_cap_N.order()
        h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: The index of N in HN is not finite or not equal to the index of H cap N in H
    try:
        if hasattr(H, 'intersect'):
            H_cap_N = H.intersect(N)
        else:
            H_cap_N = H.intersection(N)
        index_H = H.order() // H_cap_N.order()
        
        if isinstance(H, sympy.combinatorics.PermutationGroup) and isinstance(N, sympy.combinatorics.PermutationGroup):
            elements_H = list(H.generate())
            elements_N = list(N.generate())
            HN_set = set(h * n for h in elements_H for n in elements_N)
            
            gens = list(H.generators) + list(N.generators)
            HN_group = sympy.combinatorics.PermutationGroup(*gens)
            
            # If the set HN is not closed under the group operation, it is not a group.
            # In that case, the conclusion that [HN : N] is a well-defined group index fails.
            if HN_group.order() != len(HN_set):
                neg_q = True
            else:
                index_HN = HN_group.order() // N.order()
                neg_q = bool(index_HN != index_H)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: The index of H cap N in H is finite",
    "¬Q: The index of N in HN is not finite or not equal to the index of H cap N in H"
]

N_HYP = 3
NEG_Q_INDEX = 3