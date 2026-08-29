import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_elements(G):
    try:
        if hasattr(G, 'generate_dimino'):
            return list(G.generate_dimino())
        elif hasattr(G, 'elements'):
            return list(G.elements)
        elif hasattr(G, 'generate'):
            return list(G.generate())
    except Exception:
        pass
    return []

def get_order(G):
    try:
        if hasattr(G, 'order'):
            if callable(G.order):
                return G.order()
            else:
                return G.order
    except Exception:
        pass
    return len(get_elements(G))

def check_subgroup(H, G):
    try:
        if not hasattr(H, 'generators') or not hasattr(G, 'contains'):
            return False
        for h in H.generators:
            if not G.contains(h):
                return False
        return True
    except Exception:
        return False

def check_normal(N, G):
    try:
        if not hasattr(N, 'generators') or not hasattr(G, 'generators') or not hasattr(N, 'contains'):
            return False
        for n in N.generators:
            for g in G.generators:
                if not N.contains(g * n * ~g):
                    return False
        return True
    except Exception:
        return False

def check_trivial_intersection(N, H):
    try:
        if not hasattr(H, 'contains'):
            return False
        for g in get_elements(N):
            if not getattr(g, 'is_Identity', False) and H.contains(g):
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False] * 5
        G, N, H = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and check_subgroup(N, G) and check_normal(N, G)
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = isinstance(H, PermutationGroup) and check_subgroup(H, G)
    except Exception:
        h3 = False

    # H_4: N \cap H = {e}
    try:
        h4 = check_trivial_intersection(N, H)
    except Exception:
        h4 = False

    # neg_Q: G is not isomorphic to N \rtimes_\phi H
    # For finite groups with N normal, H subgroup, and N \cap H = {e}, 
    # G is isomorphic to N \rtimes H iff G = NH, which is equivalent to |G| == |N| * |H|.
    try:
        neg_q = get_order(G) != get_order(N) * get_order(H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: N \\cap H = {e}",
    "¬Q: G is not isomorphic to N ⋊ H"
]

N_HYP = 4
NEG_Q_INDEX = 4