import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = AlternatingGroup(4)
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
        G, N, H = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = bool(hasattr(G, 'order') and hasattr(G, 'elements'))
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h2 = False

    # H3: N is a subset of H
    try:
        n_elems = set(N.elements) if hasattr(N, 'elements') else set(N)
        h_elems = set(H.elements) if hasattr(H, 'elements') else set(H)
        h3 = bool(n_elems.issubset(h_elems))
    except Exception:
        h3 = False

    # H4: The index of H in G is finite
    try:
        h_elems = set(H.elements) if hasattr(H, 'elements') else set(H)
        g_order = G.order()
        h4 = bool(len(h_elems) > 0 and g_order > 0)
    except Exception:
        h4 = False

    # neg_Q: The index of H/N in G/N is NOT equal to the index of H in G
    try:
        n_elems = set(N.elements) if hasattr(N, 'elements') else set(N)
        h_elems = set(H.elements) if hasattr(H, 'elements') else set(H)
        
        index_GH = float(G.order()) / float(len(h_elems))
        
        cosets_HN = set()
        for h in h_elems:
            coset = frozenset([h * n for n in n_elems])
            cosets_HN.add(coset)
            
        len_HN = float(len(cosets_HN))
        len_GN = float(G.order()) / float(len(n_elems))
        
        index_HN_in_GN = len_GN / len_HN
        
        neg_q = bool(abs(index_HN_in_GN - index_GH) > 1e-9)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a subset of H",
    "H_4: The index of H in G is finite",
    "¬Q: The index of H/N in G/N is not equal to the index of H in G"
]

N_HYP = 4
NEG_Q_INDEX = 4