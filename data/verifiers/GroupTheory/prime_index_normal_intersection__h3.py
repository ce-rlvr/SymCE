import sympy
from sympy.combinatorics import PermutationGroup
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

def get_elements(G):
    if hasattr(G, 'elements'):
        return set(G.elements)
    elif hasattr(G, 'generate'):
        return set(G.generate())
    else:
        return set(G)

def get_order(G):
    try:
        order_attr = getattr(G, 'order')
        if callable(order_attr):
            return order_attr()
        return order_attr
    except Exception:
        return len(get_elements(G))

def check_subgroup(sub, group):
    try:
        if hasattr(sub, 'is_subgroup'):
            return sub.is_subgroup(group)
        sub_elts = get_elements(sub)
        group_elts = get_elements(group)
        return sub_elts.issubset(group_elts)
    except Exception:
        return False

def check_normal(sub, group):
    try:
        if not check_subgroup(sub, group):
            return False
        if hasattr(sub, 'is_normal'):
            return sub.is_normal(group)
        
        sub_elts = get_elements(sub)
        group_elts = get_elements(group)
        for g in group_elts:
            for n in sub_elts:
                if (g * n * ~g) not in sub_elts:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, N, H, p = witness
        elif len(witness) == 3:
            G, N, H = witness
            p = get_order(G) // get_order(N)
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        h2_ok = check_normal(N, G)
    except Exception:
        h2_ok = False

    # H_3: index of N in G is p
    try:
        h3_ok = (get_order(G) == p * get_order(N))
    except Exception:
        h3_ok = False

    # H_4: H is a subgroup of G
    try:
        h4_ok = check_subgroup(H, G)
    except Exception:
        h4_ok = False

    # ¬Q: H is not a subset of N and index of H intersect N in H is not p
    try:
        int_order = len(get_elements(H).intersection(get_elements(N)))
        h_order = get_order(H)
        neg_q_ok = (int_order != h_order) and (h_order != p * int_order)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: index of N in G is p",
    "H_4: H is a subgroup of G",
    "¬Q: H is not a subset of N and index of H intersect N in H is not p"
]

N_HYP = 4
NEG_Q_INDEX = 4