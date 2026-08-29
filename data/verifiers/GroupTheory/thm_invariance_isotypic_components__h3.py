import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_identity(G):
    for g in G.elements:
        if g.is_Identity:
            return g
    return list(G.elements)[0]**0

def normal_closure(G, H_gens):
    gens = list(H_gens)
    closure_group = PermutationGroup(gens)
    while True:
        new_gens = list(closure_group.generators)
        added = False
        for g in closure_group.generators:
            for gen in G.generators:
                conj = gen * g * ~gen
                if conj not in closure_group:
                    new_gens.append(conj)
                    added = True
        if not added:
            break
        closure_group = PermutationGroup(new_gens)
    return closure_group

def minimal_normal_subgroups(G):
    current_minimal = []
    visited = set()
    
    elements = list(G.elements)
    for g in elements:
        if g.is_Identity or g in visited:
            continue
            
        cclass = set()
        for x in elements:
            cclass.add(x * g * ~x)
        visited.update(cclass)
        
        N = normal_closure(G, [g])
        
        if any(M.is_subgroup(N) for M in current_minimal):
            continue
            
        current_minimal = [M for M in current_minimal if not N.is_subgroup(M)]
        current_minimal.append(N)
        
    return current_minimal

def is_isomorphic(G1, G2):
    if G1.order() != G2.order():
        return False
    if G1.is_abelian != G2.is_abelian:
        return False
    def order_profile(grp):
        profile = {}
        for g in grp.elements:
            o = g.order()
            profile[o] = profile.get(o, 0) + 1
        return profile
    return order_profile(G1) == order_profile(G2)

def is_semisimple(G):
    min_norms = minimal_normal_subgroups(G)
    if not min_norms:
        return True
    for N in min_norms:
        if N.is_abelian:
            return False
    return True

def compute_I_S(G, S):
    min_norms = minimal_normal_subgroups(G)
    isotypic_gens = []
    for N in min_norms:
        if is_isomorphic(N, S):
            isotypic_gens.extend(N.generators)
    if not isotypic_gens:
        return PermutationGroup([get_identity(G)])
    return PermutationGroup(isotypic_gens)

def is_automorphism(G, alpha):
    try:
        if callable(alpha):
            mapping = {g: alpha(g) for g in G.elements}
        elif isinstance(alpha, dict):
            mapping = alpha
        else:
            return False
            
        elements = set(G.elements)
        mapped_elements = set(mapping.values())
        if elements != mapped_elements:
            return False
            
        for g in G.generators:
            for h in G.elements:
                if mapping[g * h] != mapping[g] * mapping[h]:
                    return False
        return True
    except Exception:
        return False

def check_conclusion(G, S, alpha):
    I_S = compute_I_S(G, S)
    
    if callable(alpha):
        mapping = {g: alpha(g) for g in G.elements}
    else:
        mapping = alpha
        
    alpha_gens = [mapping[g] for g in I_S.generators]
    if not alpha_gens:
        alpha_I_S = PermutationGroup([get_identity(G)])
    else:
        alpha_I_S = PermutationGroup(alpha_gens)
    
    return alpha_I_S.is_subgroup(I_S) and I_S.is_subgroup(alpha_I_S)

def conditions(witness):
    try:
        G, S, alpha = witness
    except Exception:
        return [False, False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = is_semisimple(G)
    except Exception:
        h2 = False
        
    try:
        h3 = isinstance(S, PermutationGroup)
    except Exception:
        h3 = False
        
    try:
        h4 = is_automorphism(G, alpha)
    except Exception:
        h4 = False
        
    try:
        neg_q = not check_conclusion(G, S, alpha)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: I_S is the isotypic component of G corresponding to S",
    "H_4: alpha is an automorphism of G",
    "¬Q: alpha(I_S) != I_S"
]

N_HYP = 4
NEG_Q_INDEX = 4