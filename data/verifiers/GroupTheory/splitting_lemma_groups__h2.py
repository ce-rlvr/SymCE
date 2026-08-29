import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from itertools import combinations, product

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

def get_identity(group):
    for g in group.elements:
        if g * g == g:
            return g
    return None

def is_subgroup(subset, group):
    if not subset: return False
    e = get_identity(group)
    if e not in subset: return False
    subset_set = set(subset)
    for x in subset:
        for y in subset:
            if x * y not in subset_set:
                return False
    return True

def is_normal_subgroup(subset, G):
    subset_set = set(subset)
    for n in subset:
        for g in G.elements:
            if g * n * (g**-1) not in subset_set:
                return False
    return True

def get_subgroups_of_size(G, size):
    if size == 1:
        e_G = get_identity(G)
        return [PermutationGroup(e_G)]
        
    subgroups = []
    seen = set()
    elements = list(G.elements)
    e_G = get_identity(G)
    if e_G in elements:
        elements.remove(e_G)
        
    for i in range(1, min(5, len(elements) + 1)):
        for gens in combinations(elements, i):
            try:
                H_gen = PermutationGroup(*gens)
                if H_gen.order() == size:
                    elems = frozenset(H_gen.elements)
                    if elems not in seen:
                        seen.add(elems)
                        subgroups.append(H_gen)
            except Exception:
                pass
    return subgroups

def is_isomorphic_to_semidirect_product(G, K_elements, H):
    if len(list(G.elements)) != len(K_elements) * len(list(H.elements)):
        return False
        
    K_group = PermutationGroup(*K_elements)
    
    N_candidates = []
    for N in get_subgroups_of_size(G, len(K_elements)):
        if N.is_isomorphic(K_group):
            if is_normal_subgroup(list(N.elements), G):
                N_candidates.append(set(N.elements))
                
    if not N_candidates:
        return False
        
    M_candidates = []
    for M in get_subgroups_of_size(G, len(list(H.elements))):
        if M.is_isomorphic(H):
            M_candidates.append(set(M.elements))
            
    if not M_candidates:
        return False
        
    e_G = get_identity(G)
    for N_elems in N_candidates:
        for M_elems in M_candidates:
            if N_elems.intersection(M_elems) == {e_G}:
                return True
                
    return False

def check_g(g_dict, G, H, f_dict):
    G_elems = set(G.elements)
    for x in H.elements:
        if g_dict.get(x) not in G_elems:
            return False
    for x in H.elements:
        for y in H.elements:
            if g_dict[x * y] != g_dict[x] * g_dict[y]:
                return False
    for h in H.elements:
        if f_dict.get(g_dict[h]) != h:
            return False
    return True

def find_g(G, H, f_dict):
    possible_g_values = {}
    for h in H.elements:
        possible_g_values[h] = [x for x in G.elements if f_dict.get(x) == h]
        if not possible_g_values[h]:
            return False
            
    h_elements = list(H.elements)
    for g_values in product(*(possible_g_values[h] for h in h_elements)):
        g_dict = dict(zip(h_elements, g_values))
        if check_g(g_dict, G, H, f_dict):
            return True
    return False

def conditions(witness):
    try:
        if len(witness) == 4:
            G, H, f, g = witness
        elif len(witness) == 3:
            G, H, f = witness
            g = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: G and H are groups
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H2: There exists a group homomorphism g: H -> G such that f(g(h)) = h
    try:
        h2_ok = False
        f_dict = {}
        if h1_ok:
            if callable(f):
                f_dict = {x: f(x) for x in G.elements}
            elif isinstance(f, dict):
                f_dict = f
            elif isinstance(f, (list, tuple)):
                f_dict = dict(f)
                
            H_elems = set(H.elements)
            f_is_valid = True
            for x in G.elements:
                if x not in f_dict or f_dict[x] not in H_elems:
                    f_is_valid = False
                    break
                    
            if f_is_valid:
                if g is not None:
                    if callable(g):
                        g_dict = {x: g(x) for x in H.elements}
                    elif isinstance(g, dict):
                        g_dict = g
                    elif isinstance(g, (list, tuple)):
                        g_dict = dict(g)
                    else:
                        g_dict = {}
                    h2_ok = check_g(g_dict, G, H, f_dict)
                else:
                    h2_ok = find_g(G, H, f_dict)
    except Exception:
        h2_ok = False
        
    # neg_Q: G is NOT isomorphic to the semidirect product of ker(f) and H
    try:
        neg_q_ok = False
        if h1_ok and h2_ok:
            e_H = get_identity(H)
            ker_f = [x for x in G.elements if f_dict.get(x) == e_H]
            
            if not is_subgroup(ker_f, G):
                neg_q_ok = True
            else:
                is_iso = is_isomorphic_to_semidirect_product(G, ker_f, H)
                neg_q_ok = not is_iso
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: There exists a group homomorphism g: H -> G such that f(g(h)) = h for all h in H",
    "¬Q: G is not isomorphic to the semidirect product of ker(f) and H"
]

N_HYP = 2
NEG_Q_INDEX = 2