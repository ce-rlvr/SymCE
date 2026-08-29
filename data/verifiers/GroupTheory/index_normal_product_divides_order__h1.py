import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_infinite(group):
    if hasattr(group, 'order'):
        if callable(group.order):
            try:
                o = group.order()
            except Exception:
                return False
        else:
            o = group.order
        if o == float('inf') or o == sympy.oo or o == "inf":
            return True
    return False

def get_elements(group):
    if is_infinite(group):
        raise ValueError("Cannot get elements of an infinite group")
    if hasattr(group, 'generate'):
        return set(group.generate())
    elif hasattr(group, 'elements'):
        return set(group.elements)
    else:
        return set(group)

def get_order(group):
    if hasattr(group, 'order'):
        if callable(group.order):
            return group.order()
        return group.order
    return len(get_elements(group))

def is_subgroup_manual(sub, G):
    sub_elems = get_elements(sub)
    G_elems = get_elements(G)
    if not sub_elems.issubset(G_elems):
        return False
    if not sub_elems:
        return False
    for a in sub_elems:
        for b in sub_elems:
            if a * b not in sub_elems:
                return False
    return True

def is_normal_manual(N, G):
    if not is_subgroup_manual(N, G):
        return False
    N_elems = get_elements(N)
    G_elems = get_elements(G)
    for g in G_elems:
        for n in N_elems:
            if not any(g * n == n2 * g for n2 in N_elems):
                return False
    return True

def conditions(witness):
    try:
        G, H, N, HN = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        else:
            h1 = is_subgroup_manual(H, G)
    except Exception:
        h1 = False
        
    try:
        if hasattr(N, 'is_normal'):
            h2 = bool(N.is_normal(G))
        else:
            h2 = is_normal_manual(N, G)
    except Exception:
        h2 = False
        
    try:
        if hasattr(HN, 'is_product_set'):
            h3 = bool(HN.is_product_set(H, N))
        else:
            H_elems = get_elements(H)
            N_elems = get_elements(N)
            expected_HN = set(h * n for h in H_elems for n in N_elems)
            HN_elems = get_elements(HN)
            h3 = (HN_elems == expected_HN)
    except Exception:
        h3 = False
        
    try:
        if is_infinite(H) or is_infinite(N) or is_infinite(HN):
            if hasattr(HN, 'group_index'):
                index = HN.group_index(N)
            elif hasattr(HN, 'index') and not isinstance(HN, (list, tuple)):
                index = HN.index(N)
            else:
                index = None
        else:
            order_HN = get_order(HN)
            order_N = get_order(N)
            if order_N == 0:
                index = None
            else:
                index = order_HN / order_N
            
        if index is None:
            neg_q = False
        elif is_infinite(H):
            neg_q = True
        else:
            order_H = get_order(H)
            if index != int(index):
                neg_q = True
            else:
                index = int(index)
                if index == 0:
                    neg_q = True
                else:
                    neg_q = (order_H % index != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: N is a normal subgroup of G",
    "H_3: HN is the set containing all products hn where h in H and n in N",
    "neg_Q: The index of N in HN does not divide the order of H"
]

N_HYP = 3
NEG_Q_INDEX = 3