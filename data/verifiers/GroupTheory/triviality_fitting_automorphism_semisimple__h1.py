import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

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
    "H_1: G is a semisimple group",
    "H_2: Let Aut(G) be the automorphism group of G",
    "¬Q: The Fitting subgroup of Aut(G) is not the trivial subgroup"
]
N_HYP = 2
NEG_Q_INDEX = 2

def normal_closure_of_element(G, x):
    H_gens = [x]
    G_gens = G.generators
    H = PermutationGroup(H_gens)
    while True:
        old_order = H.order()
        new_gens = list(H.generators)
        for g in G_gens:
            for h in H.generators:
                conj = g * h * (~g)
                if conj not in H:
                    new_gens.append(conj)
        H = PermutationGroup(new_gens)
        if H.order() == old_order:
            break
    return H

def is_semisimple(G):
    if not isinstance(G, PermutationGroup):
        return False
    if G.order() == 1:
        return False
    for g in list(G.elements):
        if g == G.identity:
            continue
        H = normal_closure_of_element(G, g)
        if H.is_abelian:
            return False
    return True

def get_automorphism_group(G):
    elements = list(G.elements)
    n = len(elements)
    if n == 1:
        return PermutationGroup([Permutation(0)])
        
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    mult_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
            
    gens = G.generators
    gen_indices = [elem_to_idx[g] for g in gens]
    
    auts = []
    gen_orders = [g.order() for g in gens]
    candidates = []
    for order in gen_orders:
        candidates.append([i for i, e in enumerate(elements) if e.order() == order])
        
    for p in itertools.product(*candidates):
        mapping = {elem_to_idx[G.identity]: elem_to_idx[G.identity]}
        for g_idx, p_idx in zip(gen_indices, p):
            mapping[g_idx] = p_idx
            
        queue = list(zip(gen_indices, p))
        valid = True
        while queue:
            u, phi_u = queue.pop(0)
            for v in gen_indices:
                uv = mult_table[u][v]
                phi_v = mapping[v]
                phi_uv = mult_table[phi_u][phi_v]
                if uv in mapping:
                    if mapping[uv] != phi_uv:
                        valid = False
                        break
                else:
                    mapping[uv] = phi_uv
                    queue.append((uv, phi_uv))
            if not valid:
                break
                
        if valid and len(mapping) == n and len(set(mapping.values())) == n:
            is_homo = True
            for i in range(n):
                for j in range(n):
                    if mapping[mult_table[i][j]] != mult_table[mapping[i]][mapping[j]]:
                        is_homo = False
                        break
                if not is_homo:
                    break
            if is_homo:
                perm_array = [mapping[i] for i in range(n)]
                auts.append(Permutation(perm_array))
                
    if not auts:
        return PermutationGroup([Permutation(n-1)])
    return PermutationGroup(auts)

def fitting_subgroup_is_trivial(G):
    if G.order() == 1:
        return True
    for g in list(G.elements):
        if g == G.identity:
            continue
        H = normal_closure_of_element(G, g)
        if H.is_nilpotent:
            return False
    return True

def conditions(witness):
    try:
        h1 = is_semisimple(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False
        
    try:
        AutG = get_automorphism_group(witness)
        neg_q = not fitting_subgroup_is_trivial(AutG)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]