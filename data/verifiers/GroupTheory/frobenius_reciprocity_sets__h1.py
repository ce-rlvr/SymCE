import itertools
import functools
import math
import z3
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(G):
    try:
        elems = G.elements
        if callable(elems):
            return list(elems())
        return list(elems)
    except Exception:
        return list(G.generate())

def is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    try:
        G_elems = get_elements(G)
        return all(h in G_elems for h in get_elements(H))
    except Exception:
        return False

def act_Y(action_Y, g, y):
    if callable(action_Y):
        return action_Y(g, y)
    else:
        return action_Y[(g, y)]

def get_cosets(G, H):
    cosets = set()
    H_elements = get_elements(H)
    for g in get_elements(G):
        coset = frozenset([g * h for h in H_elements])
        cosets.add(coset)
    return list(cosets)

def get_Y_H(H, Y, action_Y):
    Y_H = []
    H_elements = get_elements(H)
    for y in Y:
        if all(act_Y(action_Y, h, y) == y for h in H_elements):
            Y_H.append(y)
    return Y_H

def get_equiv_maps(G, cosets, Y, action_Y):
    equiv_maps = []
    G_elements = get_elements(G)
    
    for values in itertools.product(Y, repeat=len(cosets)):
        f = dict(zip(cosets, values))
        is_equiv = True
        for g in G_elements:
            for C in cosets:
                gC = frozenset([g * x for x in C])
                if f[gC] != act_Y(action_Y, g, f[C]):
                    is_equiv = False
                    break
            if not is_equiv:
                break
        if is_equiv:
            equiv_maps.append(f)
    return equiv_maps

def check_conclusion(G, H, Y, action_Y):
    cosets = get_cosets(G, H)
    Y_H = get_Y_H(H, Y, action_Y)
    equiv_maps = get_equiv_maps(G, cosets, Y, action_Y)
    
    id_perm = None
    for g in get_elements(G):
        if g * g == g:
            id_perm = g
            break
            
    id_coset = frozenset([id_perm * h for h in get_elements(H)])
    
    # Check if the canonical map is well-defined into Y^H
    for f in equiv_maps:
        if f[id_coset] not in Y_H:
            return False
            
    # Check if the canonical map is injective
    seen = []
    for f in equiv_maps:
        val = f[id_coset]
        if val in seen:
            return False
        seen.append(val)
        
    # Check if the canonical map is surjective
    for y in Y_H:
        if y not in seen:
            return False
            
    return True

def conditions(witness):
    """
    witness is expected to be a tuple: (G, H, Y, action_Y)
    where:
      G is a PermutationGroup
      H is a PermutationGroup (subgroup of G)
      Y is an iterable representing the set Y
      action_Y is a callable or dict representing the action of G on Y
    """
    try:
        G, H, Y, action_Y = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_subgroup(H, G))
    except Exception:
        h1 = False
        
    try:
        h2 = True
        Y_list = list(Y)
        if not Y_list:
            h2 = False
        else:
            # Check that Y has unique elements
            for i in range(len(Y_list)):
                for j in range(i + 1, len(Y_list)):
                    if Y_list[i] == Y_list[j]:
                        h2 = False
            # Check that action_Y is a valid map G x Y -> Y
            if h2:
                G_elements = get_elements(G)
                for g in G_elements:
                    for y in Y_list:
                        res = act_Y(action_Y, g, y)
                        if res not in Y_list:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    try:
        q = check_conclusion(G, H, Y, action_Y)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: G/H is the set of left cosets equipped with natural left multiplication",
    "¬Q: The canonical map from G-equivariant maps to Y^H is not a bijection"
]

N_HYP = 2
NEG_Q_INDEX = 2