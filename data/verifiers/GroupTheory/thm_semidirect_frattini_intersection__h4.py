import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_subgroup(sub, G):
    return set(sub.elements).issubset(set(G.elements))

def is_normal(N, G):
    if not is_subgroup(N, G):
        return False
    N_set = set(N.elements)
    for n in N_set:
        for g in G.elements:
            if (g * n * (~g)) not in N_set:
                return False
    return True

def get_maximal_subgroups(G):
    elements = list(G.elements)
    subgroups = {}
    
    identity = None
    for g in elements:
        if g * g == g:
            identity = g
            break
            
    trivial_sub = frozenset([identity])
    subgroups[trivial_sub] = []
    queue = [trivial_sub]
    
    while queue:
        current = queue.pop(0)
        current_gens = subgroups[current]
        for g in elements:
            if g not in current:
                new_gens = current_gens + [g]
                H = PermutationGroup(new_gens)
                new_sub = frozenset(H.elements)
                if new_sub not in subgroups:
                    subgroups[new_sub] = new_gens
                    queue.append(new_sub)
                    
    G_set = frozenset(elements)
    proper_subgroups = [S for S in subgroups if S != G_set]
    maximal = []
    for M in proper_subgroups:
        is_maximal = True
        for K in proper_subgroups:
            if M != K and M.issubset(K):
                is_maximal = False
                break
        if is_maximal:
            maximal.append(M)
    return maximal

def frattini_subgroup_elements(G):
    max_subs = get_maximal_subgroups(G)
    if not max_subs:
        return frozenset(G.elements)
    return frozenset.intersection(*max_subs)

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        h2 = False
        if isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            if is_subgroup(N, G) and is_subgroup(H, G):
                if is_normal(N, G):
                    N_set = set(N.elements)
                    H_set = set(H.elements)
                    if len(N_set.intersection(H_set)) == 1:
                        if len(N.elements) * len(H.elements) == len(G.elements):
                            h2 = True
    except Exception:
        h2 = False
        
    # H_3: Φ(G) is the Frattini subgroup of G
    try:
        h3 = isinstance(G, PermutationGroup)
    except Exception:
        h3 = False
        
    # neg_Q: The intersection H ∩ Φ(G) is not a subgroup of Φ(H)
    try:
        PhiG_elements = frattini_subgroup_elements(G)
        PhiH_elements = frattini_subgroup_elements(H)
        H_elements = set(H.elements)
        H_cap_PhiG = H_elements.intersection(PhiG_elements)
        
        neg_q = not H_cap_PhiG.issubset(PhiH_elements)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_3: Φ(G) is the Frattini subgroup of G",
    "¬Q: The intersection H ∩ Φ(G) is not a subgroup of Φ(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3