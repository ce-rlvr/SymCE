import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_elements(grp):
    if hasattr(grp, 'elements'):
        return set(grp.elements)
    elif hasattr(grp, 'generate'):
        return set(grp.generate())
    else:
        return set(grp)

def get_order(grp):
    if hasattr(grp, 'order'):
        if callable(grp.order):
            return grp.order()
        else:
            return grp.order
    return len(get_elements(grp))

def is_subgroup(sub, parent):
    if not isinstance(sub, PermutationGroup):
        return False
    try:
        if hasattr(sub, 'is_subgroup'):
            res = sub.is_subgroup(parent)
            if isinstance(res, bool):
                return res
    except Exception:
        pass
    try:
        parent_elements = get_elements(parent)
        sub_elements = get_elements(sub)
        return sub_elements.issubset(parent_elements)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = is_subgroup(H, G)
    except Exception:
        h2 = False

    try:
        h3 = is_subgroup(K, G)
    except Exception:
        h3 = False

    try:
        G_order = get_order(G)
        H_order = get_order(H)
        K_order = get_order(K)
        
        H_elems = get_elements(H)
        K_elems = get_elements(K)
        
        int_elems = H_elems.intersection(K_elems)
        int_order = len(int_elems)
        
        neg_q = (H_order * K_order != G_order * int_order)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "not Q: The index of H cap K in G is not equal to the product of indices"
]

N_HYP = 3
NEG_Q_INDEX = 3