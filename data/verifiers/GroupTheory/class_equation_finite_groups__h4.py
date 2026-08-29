import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Z(G) is the center of G",
    "H_3: X is a complete set of representatives of the distinct conjugacy classes of G of size greater than 1",
    "¬Q: |G| != |Z(G)| + sum of index of C_G(x_i) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def _get_elements(obj):
    elems_attr = getattr(obj, 'elements')
    return list(elems_attr() if callable(elems_attr) else elems_attr)

def _get_order(obj):
    order_attr = getattr(obj, 'order')
    return order_attr() if callable(order_attr) else order_attr

def _get_inverse(h):
    try:
        return ~h
    except Exception:
        return h**-1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, Z, X = witness
        elif isinstance(witness, dict) and 'G' in witness and 'Z' in witness and 'X' in witness:
            G = witness['G']
            Z = witness['Z']
            X = witness['X']
        else:
            if isinstance(witness, dict) and 'G' in witness:
                G = witness['G']
            else:
                G = witness
            
            elements = _get_elements(G)
            classes = []
            seen = set()
            for g in elements:
                if g in seen:
                    continue
                c = set()
                for h in elements:
                    c.add(h * g * _get_inverse(h))
                classes.append(c)
                seen.update(c)
                
            Z = [list(c)[0] for c in classes if len(c) == 1]
            X = [list(c)[0] for c in classes if len(c) > 1]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = False
        if hasattr(G, 'elements') and hasattr(G, 'order'):
            order = _get_order(G)
            if order is not None and order > 0:
                if not math.isinf(order):
                    h1 = True
    except Exception:
        h1 = False

    # H2: Z(G) is the center of G
    try:
        h2 = False
        if h1:
            elements = _get_elements(G)
            center_elements = set()
            for g in elements:
                is_central = True
                for h in elements:
                    if h * g != g * h:
                        is_central = False
                        break
                if is_central:
                    center_elements.add(g)
            
            if hasattr(Z, 'elements'):
                Z_elements = set(_get_elements(Z))
            else:
                Z_elements = set(Z)
            h2 = (Z_elements == center_elements)
    except Exception:
        h2 = False

    # H3: X is a complete set of representatives of the distinct conjugacy classes of G of size > 1
    try:
        h3 = False
        if h1:
            elements = _get_elements(G)
            classes = []
            seen = set()
            for g in elements:
                if g in seen:
                    continue
                c = set()
                for h in elements:
                    c.add(h * g * _get_inverse(h))
                classes.append(c)
                seen.update(c)
                
            classes_gt_1 = [c for c in classes if len(c) > 1]
            
            if isinstance(X, (list, set, tuple)):
                if len(X) == len(set(X)) and len(X) == len(classes_gt_1):
                    X_set = set(X)
                    valid = True
                    for c in classes_gt_1:
                        if len(c.intersection(X_set)) != 1:
                            valid = False
                            break
                    h3 = valid
    except Exception:
        h3 = False

    # Q: |G| = |Z(G)| + sum([G : C_G(x)] for x in X)
    try:
        neg_q = False
        if h1:
            G_order = _get_order(G)
            if hasattr(Z, 'order'):
                Z_order = _get_order(Z)
            else:
                Z_order = len(Z)
                
            sum_index = 0
            elements = _get_elements(G)
            for x in X:
                c_size = 0
                for g in elements:
                    if g * x == x * g:
                        c_size += 1
                if c_size == 0:
                    raise ValueError("Centralizer is empty")
                sum_index += G_order // c_size
                
            q = (G_order == Z_order + sum_index)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]