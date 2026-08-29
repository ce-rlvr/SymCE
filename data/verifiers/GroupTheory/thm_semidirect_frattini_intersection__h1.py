import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_all_subgroups(G):
    elements = list(G.generate())
    if not elements:
        return set()
    id_el = elements[0]
    for e in elements:
        if e.is_Identity:
            id_el = e
            break
            
    subgroups = {frozenset([id_el])}
    for x in elements:
        subgroups.add(frozenset(PermutationGroup([x]).generate()))
        
    all_subs = set(subgroups)
    queue = list(subgroups)
    
    while queue:
        A = queue.pop(0)
        for B in subgroups:
            if not B.issubset(A):
                gen_elements = list(A) + list(B)
                H = frozenset(PermutationGroup(gen_elements).generate())
                if H not in all_subs:
                    all_subs.add(H)
                    queue.append(H)
    return all_subs

def frattini_subgroup(G):
    elements = list(G.generate())
    if not elements:
        return set()
    
    all_subs = get_all_subgroups(G)
    proper_subs = [S for S in all_subs if len(S) < len(elements)]
    
    maximal_subs = []
    for S in proper_subs:
        is_max = True
        for other in proper_subs:
            if S != other and S.issubset(other):
                is_max = False
                break
        if is_max:
            maximal_subs.append(S)
            
    if not maximal_subs:
        return set(elements)
        
    return set.intersection(*maximal_subs)

def is_subgroup(sub, G):
    try:
        G_els = set(G.generate())
        for g in sub.generators:
            if g not in G_els:
                return False
        return True
    except Exception:
        return False

def is_normal(N, G):
    try:
        if not is_subgroup(N, G): return False
        N_els = set(N.generate())
        for g in G.generators:
            for n in N.generators:
                if (g * n * (g**-1)) not in N_els:
                    return False
        return True
    except Exception:
        return False

def is_semidirect_product(G, N, H):
    try:
        if not is_normal(N, G): return False
        if not is_subgroup(H, G): return False
        
        N_els = set(N.generate())
        H_els = set(H.generate())
        
        intersection = N_els.intersection(H_els)
        if len(intersection) != 1:
            return False
            
        if len(N_els) * len(H_els) != len(list(G.generate())):
            return False
            
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    h1 = h2 = h3 = neg_q = False
    try:
        if len(witness) == 5:
            G, N, H, Phi_G, Phi_H = witness
            try:
                h2 = set(Phi_G.generate()) == frattini_subgroup(G)
            except Exception:
                h2 = False
            try:
                h3 = set(Phi_H.generate()) == frattini_subgroup(H)
            except Exception:
                h3 = False
        elif len(witness) == 3:
            G, N, H = witness
            try:
                Phi_G_els = frattini_subgroup(G)
                Phi_H_els = frattini_subgroup(H)
                Phi_G = PermutationGroup(list(Phi_G_els))
                Phi_H = PermutationGroup(list(Phi_H_els))
                h2 = True
                h3 = True
            except Exception:
                h2 = False
                h3 = False
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_semidirect_product(G, N, H)
    except Exception:
        h1 = False

    try:
        H_els = set(H.generate())
        Phi_G_els = set(Phi_G.generate())
        Phi_H_els = set(Phi_H.generate())
        
        intersection = H_els.intersection(Phi_G_els)
        neg_q = not intersection.issubset(Phi_H_els)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: Φ(G) is the Frattini subgroup of G",
    "H_3: Φ(H) is the Frattini subgroup of H",
    "¬Q: The intersection H ∩ Φ(G) is not a subgroup of Φ(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3