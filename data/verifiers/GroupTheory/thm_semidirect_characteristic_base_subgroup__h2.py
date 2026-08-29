import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    """Helper to get the order of a group, handling both method and property."""
    return grp.order() if callable(grp.order) else grp.order

def conditions(witness) -> list[bool]:
    try:
        G, N, H, K = witness
    except Exception:
        return [False] * 6

    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = bool(H.is_subgroup(G))
    except Exception:
        h2 = False

    # H_3: N and H have trivial intersection
    try:
        if hasattr(N, 'intersection'):
            int_grp = N.intersection(H)
            h3 = bool(get_order(int_grp) == 1)
        elif hasattr(N, 'intersect'):
            int_grp = N.intersect(H)
            h3 = bool(get_order(int_grp) == 1)
        else:
            n_elems = set(list(N.generate()))
            h_elems = set(list(H.generate()))
            h3 = bool(len(n_elems.intersection(h_elems)) == 1)
    except Exception:
        h3 = False

    # H_4: N and H generate G (since N is normal and intersection is trivial, |N|*|H| == |G|)
    try:
        h4 = bool(get_order(N) * get_order(H) == get_order(G))
    except Exception:
        h4 = False

    # H_5: K is a subgroup of N
    try:
        h5 = bool(K.is_subgroup(N))
    except Exception:
        h5 = False

    # neg_Q: K is not a normal subgroup of G
    try:
        if not K.is_subgroup(G):
            neg_q = True
        else:
            neg_q = bool(not K.is_normal(G))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: N and H have trivial intersection",
    "H_4: N and H generate G",
    "H_5: K is a subgroup of N",
    "¬Q: K is not a normal subgroup of G"
]

N_HYP = 5
NEG_Q_INDEX = 5