import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
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
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_semisimple(G):
    try:
        if not isinstance(G, PermutationGroup):
            return False
        for H in G.normal_subgroups():
            if H.order() > 1 and H.is_abelian:
                return False
        return True
    except Exception:
        return False

def is_non_abelian_simple(N):
    try:
        if not isinstance(N, PermutationGroup):
            return False
        if N.order() <= 1:
            return False
        if N.is_abelian:
            return False
        return len(N.normal_subgroups()) == 2
    except Exception:
        return False

def get_minimal_normal_subgroups(G):
    try:
        normals = G.normal_subgroups()
        non_trivial = [H for H in normals if H.order() > 1]
        minimal = []
        for H in non_trivial:
            is_min = True
            for K in non_trivial:
                if K.order() < H.order() and all(g in H for g in K.generators):
                    is_min = False
                    break
            if is_min:
                minimal.append(H)
        return minimal
    except Exception:
        return []

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, N = witness
            explicit_N = True
        else:
            G = witness
            N = None
            explicit_N = False
    except Exception:
        G = witness
        N = None
        explicit_N = False

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G is a semisimple group
    try:
        if h1:
            h2 = is_semisimple(G)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: N is not a non-abelian simple group
    try:
        if explicit_N:
            neg_q = not is_non_abelian_simple(N)
        else:
            if h1:
                min_normals = get_minimal_normal_subgroups(G)
                if not min_normals:
                    neg_q = False
                else:
                    neg_q = any(not is_non_abelian_simple(H) for H in min_normals)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "¬Q: N is not a non-abelian simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2