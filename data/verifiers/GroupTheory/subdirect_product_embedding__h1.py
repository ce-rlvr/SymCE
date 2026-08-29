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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    "H_1: N_1, ..., N_k are normal subgroups of G",
    "H_2: The intersection of N_i is the trivial subgroup",
    "¬Q: G is not isomorphic to a subgroup of the direct product of G/N_i"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_subgroup_safe(H, G):
    G_elements = set(G.elements)
    for gen in H.generators:
        if gen not in G_elements:
            return False
    return True

def is_normal_safe(H, G):
    if not is_subgroup_safe(H, G):
        return False
    H_elements = set(H.elements)
    for h in H.generators:
        for g in G.generators:
            if (g**-1 * h * g) not in H_elements:
                return False
    return True

def get_quotient_group(G, N):
    elements = list(G.elements)
    N_elements = list(N.elements)
    cosets = []
    seen = set()
    coset_map = {}
    
    for g in elements:
        if g not in seen:
            coset = frozenset(g * n for n in N_elements)
            cosets.append(coset)
            seen.update(coset)
            for c in coset:
                coset_map[c] = len(cosets) - 1
                
    m = len(cosets)
    table = [[0]*m for _ in range(m)]
    reps = [next(iter(c)) for c in cosets]
    
    for i in range(m):
        for j in range(m):
            prod = reps[i] * reps[j]
            table[i][j] = coset_map[prod]
            
    id_G = elements[0]**0
    id_H = coset_map[id_G]
    return table, id_H

def get_homomorphisms(G, H_table, id_H):
    gens = G.generators
    elements = list(G.elements)
    id_G = elements[0]**0
    
    if not gens:
        return [{id_G: id_H}]
        
    m = len(H_table)
    valid_homs = []
    
    for gen_images in itertools.product(range(m), repeat=len(gens)):
        mapping = {id_G: id_H}
        queue = [id_G]
        possible = True
        
        head = 0
        while head < len(queue):
            curr = queue[head]
            head += 1
            curr_img = mapping[curr]
            for gen, gen_img in zip(gens, gen_images):
                nxt = curr * gen
                nxt_img = H_table[curr_img][gen_img]
                if nxt in mapping:
                    if mapping[nxt] != nxt_img:
                        possible = False
                        break
                else:
                    mapping[nxt] = nxt_img
                    queue.append(nxt)
            if not possible:
                break
                
        if possible and len(mapping) == len(elements):
            is_hom = True
            for g1 in elements:
                for g2 in elements:
                    if mapping[g1 * g2] != H_table[mapping[g1]][mapping[g2]]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            if is_hom:
                valid_homs.append(mapping)
            
    return valid_homs

def embeds_in_direct_product(G, N_list):
    elements = list(G.elements)
    if not N_list:
        return len(elements) == 1
        
    homs_list = []
    id_H_list = []
    for N in N_list:
        table, id_H = get_quotient_group(G, N)
        homs = get_homomorphisms(G, table, id_H)
        homs_list.append(homs)
        id_H_list.append(id_H)
        
    id_G = elements[0]**0
    
    for f_tuple in itertools.product(*homs_list):
        kernel_trivial = True
        for g in elements:
            if g == id_G:
                continue
            maps_to_id = True
            for i, f in enumerate(f_tuple):
                if f[g] != id_H_list[i]:
                    maps_to_id = False
                    break
            if maps_to_id:
                kernel_trivial = False
                break
        if kernel_trivial:
            return True
            
    return False

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, N_list = witness
        _ = G.elements
        _ = [N.elements for N in N_list]
    except Exception:
        return [False, False, False]
        
    # H1: N_1, ..., N_k are normal subgroups of G
    try:
        h1 = True
        for N in N_list:
            if not is_normal_safe(N, G):
                h1 = False
                break
    except Exception:
        h1 = False
        
    # H2: The intersection of N_i is the trivial subgroup
    try:
        elements = list(G.elements)
        if not N_list:
            h2 = (len(elements) == 1)
        else:
            h2 = True
            id_G = elements[0]**0
            N_elements_sets = [set(N.elements) for N in N_list]
            for g in N_elements_sets[0]:
                if g == id_G:
                    continue
                in_all = True
                for N_set in N_elements_sets[1:]:
                    if g not in N_set:
                        in_all = False
                        break
                if in_all:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # neg_Q: G is NOT isomorphic to a subgroup of the direct product of G/N_i
    try:
        for N in N_list:
            if not is_normal_safe(N, G):
                raise ValueError("N is not normal, quotient is ill-defined")
                
        embeds = embeds_in_direct_product(G, N_list)
        neg_q = not embeds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]