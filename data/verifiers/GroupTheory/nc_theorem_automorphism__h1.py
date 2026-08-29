import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup_safe(H, G):
    max_deg = max(G.degree, H.degree)
    def get_array(p):
        arr = p.array_form
        if len(arr) < max_deg:
            arr = arr + list(range(len(arr), max_deg))
        return tuple(arr)
        
    G_arrays = {get_array(g) for g in G.generate()}
    for h in H.generate():
        if get_array(h) not in G_arrays:
            return False
    return True

def groups_equal(G1, G2):
    max_deg = max(G1.degree, G2.degree)
    def get_array(p):
        arr = p.array_form
        if len(arr) < max_deg:
            arr = arr + list(range(len(arr), max_deg))
        return tuple(arr)
        
    G1_arrays = {get_array(g) for g in G1.generate()}
    G2_arrays = {get_array(g) for g in G2.generate()}
    return G1_arrays == G2_arrays

def get_normalizer(G, H):
    n_elements = []
    max_deg = max(G.degree, H.degree)
    def get_array(p):
        arr = p.array_form
        if len(arr) < max_deg:
            arr = arr + list(range(len(arr), max_deg))
        return tuple(arr)
        
    H_arrays = {get_array(h) for h in H.generate()}
    for g in G.generate():
        valid = True
        for h in H.generate():
            conj = g * h * ~g
            if get_array(conj) not in H_arrays:
                valid = False
                break
        if valid:
            n_elements.append(g)
            
    if not n_elements:
        n_elements.append(G.identity)
    return PermutationGroup(n_elements)

def get_centralizer(G, H):
    c_elements = []
    max_deg = max(G.degree, H.degree)
    def get_array(p):
        arr = p.array_form
        if len(arr) < max_deg:
            arr = arr + list(range(len(arr), max_deg))
        return tuple(arr)
        
    for g in G.generate():
        valid = True
        for h in H.generate():
            if get_array(g * h) != get_array(h * g):
                valid = False
                break
        if valid:
            c_elements.append(g)
            
    if not c_elements:
        c_elements.append(G.identity)
    return PermutationGroup(c_elements)

def is_normal(N, C):
    max_deg = max(N.degree, C.degree)
    def get_array(p):
        arr = p.array_form
        if len(arr) < max_deg:
            arr = arr + list(range(len(arr), max_deg))
        return tuple(arr)
        
    C_arrays = {get_array(c) for c in C.generate()}
    for n in N.generate():
        for c in C.generate():
            conj = n * c * ~n
            if get_array(conj) not in C_arrays:
                return False
    return True

def get_quotient_group(N, C):
    max_deg = max(N.degree, C.degree)
    def get_array(p):
        arr = p.array_form
        if len(arr) < max_deg:
            arr = arr + list(range(len(arr), max_deg))
        return tuple(arr)
        
    N_elems = list(N.generate())
    C_elems = list(C.generate())
    
    cosets = []
    seen = set()
    coset_reps = []
    for n in N_elems:
        arr_n = get_array(n)
        if arr_n not in seen:
            coset_arrays = frozenset(get_array(n * c) for c in C_elems)
            cosets.append(coset_arrays)
            coset_reps.append(n)
            seen.update(coset_arrays)
            
    k = len(cosets)
    elem_to_coset = {}
    for i, coset in enumerate(cosets):
        for arr in coset:
            elem_to_coset[arr] = i
            
    perms = []
    for i in range(k):
        rep = coset_reps[i]
        p = [0] * k
        for j in range(k):
            rep_j = coset_reps[j]
            prod = rep * rep_j
            p[j] = elem_to_coset[get_array(prod)]
        perms.append(Permutation(p))
        
    return PermutationGroup(perms)

def get_automorphisms(H):
    H_elems = list(H.generate())
    n = len(H_elems)
    
    max_deg = H.degree
    def get_array(p):
        arr = p.array_form
        if len(arr) < max_deg:
            arr = arr + list(range(len(arr), max_deg))
        return tuple(arr)
        
    if n == 1:
        arr = get_array(H_elems[0])
        return [{arr: arr}]
        
    gens = H.generators
    automorphisms = []
    
    for target_gens in itertools.product(H_elems, repeat=len(gens)):
        mapping = {}
        valid = True
        
        id_elem = H.identity
        mapping[get_array(id_elem)] = id_elem
        
        for g, tg in zip(gens, target_gens):
            arr_g = get_array(g)
            if arr_g in mapping:
                if get_array(mapping[arr_g]) != get_array(tg):
                    valid = False
                    break
            else:
                mapping[arr_g] = tg
                
        if not valid:
            continue
            
        closure = [id_elem]
        idx = 0
        while idx < len(closure) and valid:
            curr = closure[idx]
            idx += 1
            for g in gens:
                nxt = curr * g
                arr_nxt = get_array(nxt)
                
                mapped_curr = mapping[get_array(curr)]
                mapped_g = mapping[get_array(g)]
                mapped_nxt = mapped_curr * mapped_g
                
                if arr_nxt in mapping:
                    if get_array(mapping[arr_nxt]) != get_array(mapped_nxt):
                        valid = False
                        break
                else:
                    mapping[arr_nxt] = mapped_nxt
                    closure.append(nxt)
                    
        if valid:
            mapped_arrays = set(get_array(v) for v in mapping.values())
            if len(mapped_arrays) == n:
                arr_mapping = {k: get_array(v) for k, v in mapping.items()}
                automorphisms.append(arr_mapping)
                
    return automorphisms

def get_AutH_group(H, automorphisms):
    H_elems = list(H.generate())
    max_deg = H.degree
    def get_array(p):
        arr = p.array_form
        if len(arr) < max_deg:
            arr = arr + list(range(len(arr), max_deg))
        return tuple(arr)
        
    elem_to_idx = {get_array(e): i for i, e in enumerate(H_elems)}
    
    perms = []
    for arr_mapping in automorphisms:
        p = [0] * len(H_elems)
        for i, e in enumerate(H_elems):
            arr_e = get_array(e)
            mapped_arr = arr_mapping[arr_e]
            p[i] = elem_to_idx[mapped_arr]
        perms.append(Permutation(p))
        
    if not perms:
        perms.append(Permutation([0]*len(H_elems)))
    return PermutationGroup(perms)

def is_isomorphic_to_subgroup(Q, AutH):
    Q_elems = list(Q.generate())
    AutH_elems = list(AutH.generate())
    
    if len(Q_elems) > len(AutH_elems):
        return False
    if len(AutH_elems) % len(Q_elems) != 0:
        return False
        
    gens = Q.generators
    
    max_deg_Q = Q.degree
    def get_array_Q(p):
        arr = p.array_form
        if len(arr) < max_deg_Q:
            arr = arr + list(range(len(arr), max_deg_Q))
        return tuple(arr)
        
    max_deg_H = AutH.degree
    def get_array_H(p):
        arr = p.array_form
        if len(arr) < max_deg_H:
            arr = arr + list(range(len(arr), max_deg_H))
        return tuple(arr)
        
    for target_gens in itertools.product(AutH_elems, repeat=len(gens)):
        mapping = {}
        valid = True
        
        id_Q = Q.identity
        id_AutH = AutH.identity
        mapping[get_array_Q(id_Q)] = id_AutH
        
        for g, tg in zip(gens, target_gens):
            arr_g = get_array_Q(g)
            if arr_g in mapping:
                if get_array_H(mapping[arr_g]) != get_array_H(tg):
                    valid = False
                    break
            else:
                mapping[arr_g] = tg
                
        if not valid:
            continue
            
        closure = [id_Q]
        idx = 0
        while idx < len(closure) and valid:
            curr = closure[idx]
            idx += 1
            for g in gens:
                nxt = curr * g
                arr_nxt = get_array_Q(nxt)
                
                mapped_curr = mapping[get_array_Q(curr)]
                mapped_g = mapping[get_array_Q(g)]
                mapped_nxt = mapped_curr * mapped_g
                
                if arr_nxt in mapping:
                    if get_array_H(mapping[arr_nxt]) != get_array_H(mapped_nxt):
                        valid = False
                        break
                else:
                    mapping[arr_nxt] = mapped_nxt
                    closure.append(nxt)
                    
        if valid:
            mapped_arrays = set(get_array_H(v) for v in mapping.values())
            if len(mapped_arrays) == len(Q_elems):
                return True
                
    return False

def conditions(witness):
    try:
        if len(witness) == 4:
            G, H, N, C = witness
            check_NC = True
        elif len(witness) == 2:
            G, H = witness
            N = get_normalizer(G, H)
            C = get_centralizer(G, H)
            check_NC = False
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        h1_ok = is_subgroup_safe(H, G)
    except Exception:
        h1_ok = False
        
    try:
        if check_NC:
            true_N = get_normalizer(G, H)
            h2_ok = groups_equal(N, true_N)
        else:
            h2_ok = True
    except Exception:
        h2_ok = False
        
    try:
        if check_NC:
            true_C = get_centralizer(G, H)
            h3_ok = groups_equal(C, true_C)
        else:
            h3_ok = True
    except Exception:
        h3_ok = False
        
    try:
        if not is_normal(N, C):
            neg_q = True
        else:
            aut_H_list = get_automorphisms(H)
            AutH = get_AutH_group(H, aut_H_list)
            Q = get_quotient_group(N, C)
            
            is_iso = is_isomorphic_to_subgroup(Q, AutH)
            neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: N_G(H) is the normalizer of H in G",
    "H_3: C_G(H) is the centralizer of H in G",
    "¬Q: The quotient group N_G(H)/C_G(H) is NOT isomorphic to a subgroup of Aut(H)"
]
N_HYP = 3
NEG_Q_INDEX = 3