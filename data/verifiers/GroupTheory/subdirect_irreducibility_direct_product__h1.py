import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
)
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

def direct_product(G, H):
    degree_G = max(G.degree, 1)
    degree_H = max(H.degree, 1)
    
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < degree_G:
            arr += list(range(len(arr), degree_G))
        arr += list(range(degree_G, degree_G + degree_H))
        gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(range(degree_G))
        h_arr = list(h.array_form)
        if len(h_arr) < degree_H:
            h_arr += list(range(len(h_arr), degree_H))
        arr += [x + degree_G for x in h_arr]
        gens.append(Permutation(arr))
        
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def is_subdirectly_irreducible(grp):
    try:
        elements = list(grp.elements)
    except Exception:
        return False
        
    if len(elements) <= 1:
        return False
        
    id_elem = None
    for e in elements:
        if e * e == e:
            id_elem = e
            break
    if id_elem is None:
        return False
            
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        c = set()
        for g in elements:
            c.add(g * x * (g ** -1))
        classes.append(c)
        unseen -= c
        
    id_class = {id_elem}
    other_classes = [c for c in classes if c != id_class]
    
    if not other_classes:
        return False
        
    normal_closures = []
    for c in other_classes:
        closure = {id_elem}
        queue = [id_elem]
        gens = list(c)
        while queue:
            x = queue.pop(0)
            for g in gens:
                xg = x * g
                if xg not in closure:
                    closure.add(xg)
                    queue.append(xg)
        normal_closures.append(closure)
        
    intersection = set(normal_closures[0])
    for nc in normal_closures[1:]:
        intersection = intersection.intersection(nc)
        if len(intersection) == 1:
            return False
            
    return len(intersection) > 1

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is non-trivial
    try:
        if hasattr(G, 'order'):
            if callable(G.order):
                h1 = G.order() > 1
            else:
                h1 = G.order > 1
        else:
            h1 = len(list(G.elements)) > 1
    except Exception:
        h1 = False

    # H2: H is non-trivial
    try:
        if hasattr(H, 'order'):
            if callable(H.order):
                h2 = H.order() > 1
            else:
                h2 = H.order > 1
        else:
            h2 = len(list(H.elements)) > 1
    except Exception:
        h2 = False

    # neg_Q: G x H is subdirectly irreducible
    try:
        GxH = direct_product(G, H)
        neg_q = is_subdirectly_irreducible(GxH)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is non-trivial",
    "H_2: H is non-trivial",
    "¬Q: The direct product G x H is subdirectly irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2