import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The center of N is trivial",
    "H_3: Every automorphism of N is an inner automorphism",
    "¬Q: G is not isomorphic to the direct product N \\times C_G(N)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        elements_G = list(G.generate())
        elements_G_set = set(elements_G)
        id_G = next(x for x in elements_G if x.is_Identity)
    except Exception:
        return [False, False, False, False]
        
    try:
        elements_N = list(N.generate())
        elements_N_set = set(elements_N)
        gens_N = N.generators
        gens_G = G.generators
        id_N = next(x for x in elements_N if x.is_Identity)
    except Exception:
        return [False, False, False, False]

    # H1: N is a normal subgroup of G
    try:
        is_sub = all(g in elements_G_set for g in gens_N)
        is_normal = False
        if is_sub:
            is_normal = True
            for h in gens_N:
                for g in gens_G:
                    if (g * h * ~g) not in elements_N_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
        h1 = is_normal
    except Exception:
        h1 = False

    # H2: The center of N is trivial
    try:
        z_count = 0
        for x in elements_N:
            if all(x * g == g * x for g in gens_N):
                z_count += 1
        h2 = (z_count == 1)
    except Exception:
        h2 = False

    # H3: Every automorphism of N is an inner automorphism
    try:
        n_elements = len(elements_N)
        if n_elements == 1:
            h3 = True
        else:
            gen_orders = [g.order() for g in gens_N]
            elements_by_order = {}
            for x in elements_N:
                elements_by_order.setdefault(x.order(), []).append(x)
                
            valid_cands_lists = [elements_by_order.get(o, []) for o in gen_orders]
            
            aut_count = 0
            for cands in itertools.product(*valid_cands_lists):
                mapping = {id_N: id_N}
                queue = [id_N]
                
                is_hom = True
                while queue:
                    curr = queue.pop(0)
                    curr_img = mapping[curr]
                    for i, g in enumerate(gens_N):
                        nxt = curr * g
                        nxt_img = curr_img * cands[i]
                        if nxt in mapping:
                            if mapping[nxt] != nxt_img:
                                is_hom = False
                                break
                        else:
                            mapping[nxt] = nxt_img
                            queue.append(nxt)
                    if not is_hom:
                        break
                
                if is_hom and len(set(mapping.values())) == n_elements:
                    aut_count += 1
                    
            z_count = 0
            for x in elements_N:
                if all(x * g == g * x for g in gens_N):
                    z_count += 1
            inn_count = n_elements // z_count
            
            h3 = (aut_count == inn_count)
    except Exception:
        h3 = False

    # neg_Q: G is NOT isomorphic to N \times C_G(N)
    try:
        c_g_n_elements = []
        for g in elements_G:
            if all(g * n == n * g for n in gens_N):
                c_g_n_elements.append(g)
        
        if len(elements_G) != len(elements_N) * len(c_g_n_elements):
            neg_q = True
        else:
            intersection_size = sum(1 for g in c_g_n_elements if g in elements_N_set)
            if intersection_size == 1:
                neg_q = False
            else:
                C_G_N = PermutationGroup(c_g_n_elements) if c_g_n_elements else PermutationGroup([id_G])
                degree_N = N.degree
                degree_C = G.degree
                
                gens_prod = []
                for g in gens_N:
                    arr = list(g.array_form)
                    if len(arr) < degree_N:
                        arr += list(range(len(arr), degree_N))
                    new_array = arr + list(range(degree_N, degree_N + degree_C))
                    gens_prod.append(Permutation(new_array))
                    
                for g in C_G_N.generators:
                    arr = list(g.array_form)
                    if len(arr) < degree_C:
                        arr += list(range(len(arr), degree_C))
                    new_array = list(range(degree_N)) + [x + degree_N for x in arr]
                    gens_prod.append(Permutation(new_array))
                    
                if not gens_prod:
                    gens_prod = [Permutation()]
                    
                N_times_C = PermutationGroup(gens_prod)
                is_iso = G.is_isomorphic(N_times_C)
                neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]