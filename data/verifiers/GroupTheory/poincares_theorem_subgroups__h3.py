import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            if hasattr(H, 'is_subgroup'):
                h2 = bool(H.is_subgroup(G))
            else:
                h2 = bool(all(g in G for g in H.generators))
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: The index of H in G is finite
    try:
        if h1 and h2:
            index_H = G.order() / H.order()
            h3 = bool(index_H > 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: The index of K in G is finite
    try:
        if h1:
            if hasattr(K, 'order'):
                size_K = K.order()
            elif hasattr(K, '__len__'):
                size_K = len(K)
            elif hasattr(K, 'generate'):
                size_K = len(set(K.generate()))
            else:
                size_K = 0
            
            if size_K > 0:
                index_K = G.order() / size_K
                h4 = bool(index_K > 0)
            else:
                h4 = False
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: The intersection of H and K does not have finite index in G, or its index exceeds the product of indices
    try:
        if hasattr(H, 'elements'):
            elems_H = set(H.elements)
        elif hasattr(H, 'generate'):
            elems_H = set(H.generate())
        else:
            elems_H = set(H)
            
        if hasattr(K, 'elements'):
            elems_K = set(K.elements)
        elif hasattr(K, 'generate'):
            elems_K = set(K.generate())
        else:
            elems_K = set(K)
            
        int_HK = elems_H.intersection(elems_K)
        size_int = len(int_HK)
        size_H = len(elems_H)
        size_K = len(elems_K)
        
        if size_H == 0 or size_K == 0:
            neg_q = False
        elif size_int == 0:
            # If intersection is empty, index is infinite, so the conclusion fails.
            neg_q = True
        else:
            # Conclusion: index(H \cap K) <= index(H) * index(K)
            # Negation: index(H \cap K) > index(H) * index(K)
            # Algebraically equivalent to: |H| * |K| > |G| * |H \cap K| (avoids floating point issues)
            neg_q = bool((size_H * size_K) > (G.order() * size_int))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: The index of H in G is finite",
    "H_4: The index of K in G is finite",
    "¬Q: The intersection of H and K does not have finite index in G, or its index exceeds the product of indices"
]

N_HYP = 4
NEG_Q_INDEX = 4