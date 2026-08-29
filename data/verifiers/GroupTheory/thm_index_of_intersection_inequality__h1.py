import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, oo
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_order(grp):
    if hasattr(grp, 'order'):
        try:
            return grp.order()
        except Exception:
            pass
    if hasattr(grp, '__len__'):
        try:
            return len(grp)
        except Exception:
            pass
    return oo

def get_intersection(H, K):
    if hasattr(H, 'intersection'):
        try:
            res = H.intersection(K)
            if res is not None: return res
        except Exception:
            pass
    if hasattr(H, 'intersect'):
        try:
            res = H.intersect(K)
            if res is not None: return res
        except Exception:
            pass
    if hasattr(H, 'generate') and hasattr(K, 'generate'):
        try:
            set_H = set(H.generate())
            set_K = set(K.generate())
            common = set_H.intersection(set_K)
            return PermutationGroup(list(common))
        except Exception:
            pass
    if isinstance(H, (list, set, tuple)) and isinstance(K, (list, set, tuple)):
        return list(set(H).intersection(set(K)))
    raise ValueError("Cannot compute intersection")

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        elif isinstance(H, (list, set, tuple)) and isinstance(G, (list, set, tuple)):
            h1 = set(H).issubset(set(G))
        else:
            h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    # H2: K is a subgroup of G
    try:
        if hasattr(K, 'is_subgroup'):
            h2 = bool(K.is_subgroup(G))
        elif isinstance(K, (list, set, tuple)) and isinstance(G, (list, set, tuple)):
            h2 = set(K).issubset(set(G))
        else:
            h2 = all(g in G for g in K.generators)
    except Exception:
        h2 = False

    # H3: index of K in G is finite
    try:
        oG = get_order(G)
        oK = get_order(K)
        if oG == oo:
            if hasattr(G, 'index'):
                idx_GK = G.index(K)
            else:
                idx_GK = oo
        elif oK == oo:
            idx_GK = 0
        else:
            idx_GK = sympy.Rational(oG, oK)
            
        h3 = (idx_GK != oo)
    except Exception:
        h3 = False

    # neg_Q: index of H cap K in H is infinite or greater than index of K in G
    try:
        H_cap_K = get_intersection(H, K)
        oH = get_order(H)
        oHK = get_order(H_cap_K)
        if oH == oo:
            if hasattr(H, 'index'):
                idx_H_HK = H.index(H_cap_K)
            else:
                idx_H_HK = oo
        elif oHK == oo:
            idx_H_HK = 0
        else:
            idx_H_HK = sympy.Rational(oH, oHK)
            
        if idx_H_HK == oo:
            neg_q = True
        else:
            neg_q = bool(idx_H_HK > idx_GK)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "H_3: The index of K in G is finite",
    "not Q: The index of H cap K in H is infinite or greater than the index of K in G"
]

N_HYP = 3
NEG_Q_INDEX = 3