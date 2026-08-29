import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elems(group_obj):
    try:
        if hasattr(group_obj, 'generate') and callable(group_obj.generate):
            return frozenset(group_obj.generate())
    except Exception:
        pass
    try:
        if hasattr(group_obj, 'elements'):
            return frozenset(group_obj.elements)
    except Exception:
        pass
    return frozenset(group_obj)

def closure(existing_group, new_gens):
    s = set(existing_group)
    new_elems = []
    for g in new_gens:
        if g not in s:
            s.add(g)
            new_elems.append(g)
            
    while new_elems:
        next_new = []
        for x in new_elems:
            for y in list(s):
                xy = x * y
                if xy not in s:
                    s.add(xy)
                    next_new.append(xy)
                yx = y * x
                if yx not in s:
                    s.add(yx)
                    next_new.append(yx)
        new_elems = next_new
    return frozenset(s)

def get_all_subgroups(G_elems, identity):
    trivial_sg = frozenset([identity])
    all_subgroups = {trivial_sg}
    queue = [trivial_sg]
    
    while queue:
        curr = queue.pop(0)
        for g in G_elems:
            if g not in curr:
                new_sg = closure(curr, [g])
                if new_sg not in all_subgroups:
                    all_subgroups.add(new_sg)
                    queue.append(new_sg)
    return all_subgroups

def frattini(group_elems, all_subgroups):
    proper_subgroups = [sg for sg in all_subgroups if sg.issubset(group_elems) and len(sg) < len(group_elems)]
    if not proper_subgroups:
        return group_elems
    
    maximal_subgroups = []
    for M in proper_subgroups:
        is_maximal = True
        for K in proper_subgroups:
            if M != K and M.issubset(K):
                is_maximal = False
                break
        if is_maximal:
            maximal_subgroups.append(M)
            
    if not maximal_subgroups:
        return group_elems
        
    frat = set(maximal_subgroups[0])
    for M in maximal_subgroups[1:]:
        frat = frat.intersection(M)
    return frozenset(frat)

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        G_elems = get_elems(G)
        h1 = len(G_elems) > 0
    except Exception:
        h1 = False
        
    # H2: G is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        N_elems = get_elems(N)
        H_elems = get_elems(H)
        
        is_N_sub = N_elems.issubset(G_elems)
        is_H_sub = H_elems.issubset(G_elems)
        
        # N is normal in G
        is_N_normal = True
        for g in G_elems:
            try:
                g_inv = ~g
            except Exception:
                g_inv = g**-1
            for n in N_elems:
                if g * n * g_inv not in N_elems:
                    is_N_normal = False
                    break
            if not is_N_normal:
                break
                
        # N int H = {e}
        int_NH = N_elems.intersection(H_elems)
        identity = list(G_elems)[0]**0
        is_trivial_int = (len(int_NH) == 1 and identity in int_NH)
        
        # NH = G
        NH_set = set(n * h for n in N_elems for h in H_elems)
        is_NH_G = (NH_set == G_elems)
        
        h2 = is_N_sub and is_H_sub and is_N_normal and is_trivial_int and is_NH_G
    except Exception:
        h2 = False
        
    # H3: Φ(H) is the Frattini subgroup of H
    try:
        H_elems = get_elems(H)
        h3 = len(H_elems) > 0
    except Exception:
        h3 = False
        
    # neg_Q: H ∩ Φ(G) is not a subgroup of Φ(H)
    try:
        identity_G = list(G_elems)[0]**0
        subs_G = get_all_subgroups(G_elems, identity_G)
        phi_G = frattini(G_elems, subs_G)
        
        identity_H = list(H_elems)[0]**0
        subs_H = get_all_subgroups(H_elems, identity_H)
        phi_H = frattini(H_elems, subs_H)
        
        intersection = H_elems.intersection(phi_G)
        neg_q = not intersection.issubset(phi_H)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_3: Φ(H) is the Frattini subgroup of H",
    "¬Q: H ∩ Φ(G) is not a subgroup of Φ(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3