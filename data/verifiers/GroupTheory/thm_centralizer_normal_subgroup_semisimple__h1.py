import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.group_constructs import DirectProduct
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DirectProduct(CyclicGroup(2), CyclicGroup(2))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Helper functions to safely handle SymPy properties vs methods
def get_order(grp):
    order = grp.order
    if callable(order):
        return order()
    return order

def get_generators(grp):
    gens = grp.generators
    if callable(gens):
        return gens()
    return gens

def is_abelian(grp):
    ab = grp.is_abelian
    if callable(ab):
        return ab()
    return ab

def get_elem_order(g):
    order = g.order
    if callable(order):
        return order()
    return order

def intersection_is_trivial(H, K):
    for h in H.generate():
        if h != h**2 and K.contains(h):
            return False
    return True

def is_subgroup(G, H):
    for h in get_generators(H):
        if not G.contains(h):
            return False
    return True

def is_normal(G, H):
    if not is_subgroup(G, H):
        return False
    for g in get_generators(G):
        g_inv = g**-1
        for h in get_generators(H):
            if not H.contains(g_inv * h * g):
                return False
            if not H.contains(g * h * g_inv):
                return False
    return True

def conditions(witness):
    try:
        G, N, M = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a semisimple group
    # A finite group is semisimple if it is a direct product of simple groups.
    # Equivalently, every normal subgroup has a normal complement.
    try:
        if is_abelian(G):
            h1 = True
            for g in G.generate():
                if g == g**2:
                    continue
                factors = factorint(get_elem_order(g))
                if any(v > 1 for v in factors.values()):
                    h1 = False
                    break
        else:
            if hasattr(G, 'normal_subgroups'):
                ns_attr = G.normal_subgroups
                normal_subs = ns_attr() if callable(ns_attr) else ns_attr
                order_G = get_order(G)
                h1 = True
                for H in normal_subs:
                    has_complement = False
                    order_H = get_order(H)
                    for K in normal_subs:
                        if order_H * get_order(K) == order_G:
                            if intersection_is_trivial(H, K):
                                has_complement = True
                                break
                    if not has_complement:
                        h1 = False
                        break
            else:
                h1 = False
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = is_normal(G, N)
    except Exception:
        h2 = False

    # H3: M is the normal complement of N in G
    try:
        h3 = False
        if is_normal(G, M):
            if get_order(N) * get_order(M) == get_order(G):
                if intersection_is_trivial(N, M):
                    h3 = True
    except Exception:
        h3 = False

    # neg_Q: C_G(N) != M
    try:
        c_elements = set()
        gens = get_generators(N)
        for g in G.generate():
            commutes = True
            for n in gens:
                if g * n != n * g:
                    commutes = False
                    break
            if commutes:
                c_elements.add(g)
        
        m_elements = set(M.generate())
        neg_q = c_elements != m_elements
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: N is a normal subgroup of G",
    "H_3: M is the normal complement of N in G",
    "¬Q: C_G(N) != M"
]

N_HYP = 3
NEG_Q_INDEX = 3