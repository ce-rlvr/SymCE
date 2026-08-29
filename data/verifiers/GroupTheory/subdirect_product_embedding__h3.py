import math
import itertools
import functools
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for witness expressions
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

def get_group_order(G):
    if callable(G.order):
        return G.order()
    return G.order

def get_order(p):
    if callable(p.order):
        return p.order()
    return p.order

def get_identity(G):
    try:
        return G.identity
    except Exception:
        if not G.generators:
            return Permutation()
        g = G.generators[0]
        return g ** get_order(g)

def is_group(G):
    return isinstance(G, PermutationGroup)

def is_normal(G, N):
    try:
        if not G.is_subgroup(N):
            return False
        return G.is_normal(N)
    except Exception:
        pass
        
    try:
        def normalize(p):
            arr = list(p.array_form)
            while arr and arr[-1] == len(arr) - 1:
                arr.pop()
            return tuple(arr)
            
        G_elems = {normalize(g) for g in G.generate()}
        N_elems = {normalize(n) for n in N.generate()}
        if not N_elems.issubset(G_elems):
            return False
            
        for g in G.generators:
            g_inv = g ** -1
            for n in N.generators:
                c1 = normalize(g * n * g_inv)
                c2 = normalize(g_inv * n * g)
                if c1 not in N_elems or c2 not in N_elems:
                    return False
        return True
    except Exception:
        return False

def are_normal_subgroups(G, N_list):
    if not isinstance(N_list, (list, tuple)):
        return False
    if len(N_list) == 0:
        return False
    for N in N_list:
        if not is_group(N):
            return False
        if not is_normal(G, N):
            return False
    return True

def quotient_group(G, N):
    def normalize(p):
        arr = list(p.array_form)
        while arr and arr[-1] == len(arr) - 1:
            arr.pop()
        return tuple(arr)
        
    G_elems = list(G.generate())
    N_elems = list(N.generate())
    
    cosets = []
    seen = set()
    coset_reps = []
    
    for g in G_elems:
        norm_g = normalize(g)
        if norm_g in seen:
            continue
            
        coset_tuples = frozenset(normalize(g * n) for n in N_elems)
        cosets.append(coset_tuples)
        seen.update(coset_tuples)
        coset_reps.append(g)
        
    perms = []
    for gen in G.generators:
        p = []
        for rep in coset_reps:
            gc = gen * rep
            norm_gc = normalize(gc)
            for j, C in enumerate(cosets):
                if norm_gc in C:
                    p.append(j)
                    break
        perms.append(Permutation(p))
        
    if not perms:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(perms)

def direct_product(groups):
    if not groups:
        return PermutationGroup([Permutation(0)])
        
    degrees = []
    for G in groups:
        d = G.degree
        for g in G.generators:
            if g.size > d:
                d = g.size
        if d == 0:
            d = 1
        degrees.append(d)
        
    offsets = [0]
    for d in degrees[:-1]:
        offsets.append(offsets[-1] + d)
        
    total_degree = sum(degrees)
    
    new_gens = []
    for i, G in enumerate(groups):
        offset = offsets[i]
        d = degrees[i]
        for gen in G.generators:
            arr = list(range(total_degree))
            for j in range(d):
                if j < gen.size:
                    arr[offset + j] = offset + gen(j)
                else:
                    arr[offset + j] = offset + j
            new_gens.append(Permutation(arr))
            
    if not new_gens:
        return PermutationGroup([Permutation(total_degree - 1)])
    return PermutationGroup(new_gens)

def embeds_in(G, P):
    def normalize(p):
        arr = list(p.array_form)
        while arr and arr[-1] == len(arr) - 1:
            arr.pop()
        return tuple(arr)
        
    if get_group_order(G) > get_group_order(P):
        return False
        
    G_gens = G.generators
    if not G_gens:
        return True
        
    r = len(G_gens)
    P_elems = list(P.generate())
    
    G_id = get_identity(G)
    P_id = get_identity(P)
    
    for p_tuple in itertools.product(P_elems, repeat=r):
        match = True
        for g, p in zip(G_gens, p_tuple):
            if get_order(g) != get_order(p):
                match = False
                break
        if not match:
            continue
            
        mapping = {normalize(G_id): P_id}
        queue = [G_id]
        is_hom = True
        
        while queue:
            curr_g = queue.pop(0)
            curr_h = mapping[normalize(curr_g)]
            
            for g_gen, p_gen in zip(G_gens, p_tuple):
                next_g = curr_g * g_gen
                next_h = curr_h * p_gen
                
                norm_next_g = normalize(next_g)
                norm_next_h = normalize(next_h)
                
                if norm_next_g in mapping:
                    if normalize(mapping[norm_next_g]) != norm_next_h:
                        is_hom = False
                        break
                else:
                    mapping[norm_next_g] = next_h
                    queue.append(next_g)
            if not is_hom:
                break
                
        if is_hom:
            image_set = {normalize(h) for h in mapping.values()}
            if len(image_set) == get_group_order(G):
                return True
                
    return False

def neg_q(G, N_list):
    quotients = []
    for N in N_list:
        Q_grp = quotient_group(G, N)
        quotients.append(Q_grp)
        
    P = direct_product(quotients)
    return not embeds_in(G, P)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        G, N_list = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False
        
    try:
        h2 = h1 and are_normal_subgroups(G, N_list)
    except Exception:
        h2 = False
        
    try:
        if h1 and h2:
            nq = neg_q(G, N_list)
        else:
            nq = False
    except Exception:
        nq = False
        
    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N_1, ..., N_k are normal subgroups of G",
    "¬Q: G is not isomorphic to a subgroup of the direct product of G/N_i"
]
N_HYP = 2
NEG_Q_INDEX = 2