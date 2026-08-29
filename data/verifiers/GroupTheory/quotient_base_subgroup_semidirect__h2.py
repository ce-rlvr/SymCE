import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

# Helper functions for safe SymPy API usage
def get_order(G):
    return G.order() if callable(G.order) else G.order

def get_generators(G):
    if callable(G.generators):
        return list(G.generators())
    return list(G.generators)

def is_subgroup(H, G):
    if hasattr(H, 'is_subgroup'):
        try:
            return H.is_subgroup(G)
        except Exception:
            pass
    for h in get_generators(H):
        if h not in G:
            return False
    return True

def is_normal_subgroup(H, G):
    if hasattr(H, 'is_normal'):
        try:
            return H.is_normal(G)
        except Exception:
            pass
    for g in get_generators(G):
        for h in get_generators(H):
            if (g * h * ~g) not in H:
                return False
    return True

def group_intersection(G1, G2):
    if hasattr(G1, 'intersection'):
        try:
            return G1.intersection(G2)
        except Exception:
            pass
    if hasattr(G1, 'intersect'):
        try:
            return G1.intersect(G2)
        except Exception:
            pass
    
    if hasattr(G1, 'elements'):
        elems = list(G1.elements)
    else:
        elems = list(G1.generate())
        
    elements = [g for g in elems if g in G2]
    if not elements:
        elements = [get_generators(G1)[0]**0]
    return PermutationGroup(elements)

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False]*5 + [False]
        G, N, H, K = witness
    except Exception:
        return [False]*5 + [False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = is_subgroup(H, G)
    except Exception:
        h2 = False
        
    try:
        # G is the internal semidirect product of N and H
        # This requires N and H to be subgroups, trivial intersection, product is G, 
        # and at least one of them is normal.
        cond_sub = is_subgroup(N, G) and is_subgroup(H, G)
        int_NH = group_intersection(N, H)
        cond_int = (get_order(int_NH) == 1)
        cond_prod = (get_order(N) * get_order(H) == get_order(G))
        cond_norm = is_normal_subgroup(N, G) or is_normal_subgroup(H, G)
        h3 = cond_sub and cond_int and cond_prod and cond_norm
    except Exception:
        h3 = False
        
    try:
        h4 = is_subgroup(K, G) and is_normal_subgroup(K, G)
    except Exception:
        h4 = False
        
    try:
        h5 = is_subgroup(K, N)
    except Exception:
        h5 = False
        
    try:
        # Conclusion: G/K is isomorphic to the internal semidirect product of the normal subgroup N/K and the subgroup HK/K.
        # For this to be true, N/K must be normal in G/K (which means N must be normal in G).
        is_N_normal = is_normal_subgroup(N, G)
        
        HK_gens = get_generators(H) + get_generators(K)
        HK = PermutationGroup(HK_gens)
        
        # N/K \cap HK/K must be trivial, meaning N \cap HK == K
        int_N_HK = group_intersection(N, HK)
        is_intersect_K = (get_order(int_N_HK) == get_order(K)) and is_subgroup(K, int_N_HK)
        
        # The product (N/K)(HK/K) must be G/K, meaning |N| * |HK| / |K| == |G|
        is_prod_G = (get_order(N) * get_order(HK) // get_order(K) == get_order(G))
        
        Q = is_N_normal and is_intersect_K and is_prod_G
        neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [h1, h2, h3, h4, h5, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "H_4: K is a normal subgroup of G",
    "H_5: K is a subgroup of N",
    "¬Q: G/K is not isomorphic to the internal semidirect product of the normal subgroup N/K and the subgroup HK/K"
]

N_HYP = 5
NEG_Q_INDEX = 5