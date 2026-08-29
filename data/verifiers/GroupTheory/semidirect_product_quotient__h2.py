import sympy
from sympy.combinatorics import PermutationGroup
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

def _is_subgroup(G, H):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    g_elements = set(G.generate_dimino())
    return all(h in g_elements for h in H.generators)

def _is_normal_subgroup(G, N):
    try:
        if hasattr(G, 'is_normal'):
            return G.is_normal(N)
    except Exception:
        pass
    n_elements = set(N.generate_dimino())
    for g in G.generate_dimino():
        g_inv = ~g
        for n in N.generators:
            if g * n * g_inv not in n_elements:
                return False
    return True

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False] * 4 + [False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and _is_subgroup(G, H)
    except Exception:
        h2 = False
        
    # H3: G = NH
    try:
        if isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            nh_set = set(n * h for n in N.generate_dimino() for h in H.generate_dimino())
            g_set = set(G.generate_dimino())
            h3 = (nh_set == g_set)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # H4: N \cap H = {e}
    try:
        if isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            n_set = set(N.generate_dimino())
            h_set = set(H.generate_dimino())
            intersection = n_set.intersection(h_set)
            id_elem = None
            for e in G.generate_dimino():
                if e * e == e:
                    id_elem = e
                    break
            h4 = (len(intersection) == 1 and id_elem in intersection)
        else:
            h4 = False
    except Exception:
        h4 = False
        
    # neg_Q: G/N \cong H is FALSE
    try:
        if not isinstance(N, PermutationGroup) or not _is_subgroup(G, N):
            neg_q = True
        elif not _is_normal_subgroup(G, N):
            # If N is not normal, G/N is not a group, so it cannot be isomorphic to H.
            neg_q = True
        else:
            # N is normal, so G/N is a valid group.
            try:
                g_order = G.order()
                n_order = N.order()
                h_order = H.order()
            except Exception:
                g_order = len(list(G.generate_dimino()))
                n_order = len(list(N.generate_dimino()))
                h_order = len(list(H.generate_dimino()))
                
            if g_order // n_order != h_order:
                neg_q = True
            else:
                if hasattr(G, 'quotient_group'):
                    Q = G.quotient_group(N)
                    neg_q = not Q.is_isomorphic(H)
                else:
                    # By the Second Isomorphism Theorem, if G=NH, N \cap H = {e}, and N is normal,
                    # then G/N is isomorphic to H.
                    if h3 and h4:
                        neg_q = False
                    else:
                        # Conservative fallback if we cannot compute the quotient group directly
                        neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: G = NH",
    "H_4: N \\cap H = \\{e\\}",
    "¬Q: G/N is not isomorphic to H"
]

N_HYP = 4
NEG_Q_INDEX = 4