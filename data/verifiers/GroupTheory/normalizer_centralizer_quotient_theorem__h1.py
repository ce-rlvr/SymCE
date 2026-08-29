import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import product

# Top-level setup for witness evaluation
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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: N_G(H) is the normalizer of H in G",
    "H_3: C_G(H) is the centralizer of H in G",
    "¬Q: C_G(H) is not a normal subgroup of N_G(H) or N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)"
]

def get_normalizer(G, H):
    n_gens = []
    H_elements = set(H.elements)
    for g in G.elements:
        if all(g * h * ~g in H_elements for h in H.generators):
            n_gens.append(g)
    if not n_gens:
        return PermutationGroup([G.identity])
    return PermutationGroup(n_gens)

def get_centralizer(G, H):
    c_gens = []
    for g in G.elements:
        if all(g * h * ~g == h for h in H.generators):
            c_gens.append(g)
    if not c_gens:
        return PermutationGroup([G.identity])
    return PermutationGroup(c_gens)

def get_automorphism_group(H):
    elements = list(H.elements)
    n = len(elements)
    if n == 1:
        return PermutationGroup([Permutation([0])])
        
    idx = {e: i for i, e in enumerate(elements)}
    
    mult = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult[i][j] = idx[elements[i] * elements[j]]
            
    gens = H.generators
    gen_indices = [idx[g] for g in gens]
    
    aut_perms = []
    for target_indices in product(range(n), repeat=len(gens)):
        visited = set(target_indices)
        queue = list(target_indices)
        while queue:
            curr = queue.pop(0)
            for g in target_indices:
                nxt = mult[curr][g]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        if len(visited) != n:
            continue
            
        mapping = {idx[H.identity]: idx[H.identity]}
        valid = True
        for i, g in enumerate(gen_indices):
            if g in mapping:
                if mapping[g] != target_indices[i]:
                    valid = False
                    break
            else:
                mapping[g] = target_indices[i]
                
        if not valid:
            continue
            
        queue = [idx[H.identity]]
        while queue and valid:
            curr = queue.pop(0)
            for i, g in enumerate(gen_indices):
                nxt = mult[curr][g]
                mapped_nxt = mult[mapping[curr]][mapping[g]]
                if nxt in mapping:
                    if mapping[nxt] != mapped_nxt:
                        valid = False
                        break
                else:
                    mapping[nxt] = mapped_nxt
                    queue.append(nxt)
                    
        if valid and len(mapping) == n:
            perm_array = [mapping[i] for i in range(n)]
            aut_perms.append(Permutation(perm_array))
            
    if not aut_perms:
        return PermutationGroup([Permutation(list(range(n)))])
    return PermutationGroup(aut_perms)

def get_quotient_group(N, C):
    N_elements = list(N.elements)
    C_elements = set(C.elements)
    
    cosets = []
    coset_reps = []
    seen = set()
    
    for n in N_elements:
        if n in seen:
            continue
        coset = set(n * c for c in C_elements)
        cosets.append(coset)
        coset_reps.append(n)
        seen.update(coset)
        
    k = len(cosets)
    rep_to_idx = {}
    for i, rep in enumerate(coset_reps):
        for c in C_elements:
            rep_to_idx[rep * c] = i
            
    perms = []
    for i in range(k):
        perm = []
        for j in range(k):
            prod = coset_reps[i] * coset_reps[j]
            perm.append(rep_to_idx[prod])
        perms.append(Permutation(perm))
        
    return PermutationGroup(perms)

def check_conclusion(G, H, N, C):
    if not C.is_subgroup(N):
        return False
    if not C.is_normal(N):
        return False
        
    NC = get_quotient_group(N, C)
    AutH = get_automorphism_group(H)
    
    if AutH.order() % NC.order() != 0:
        return False
        
    if NC.order() == 1:
        return True
        
    NC_elements = list(NC.elements)
    NC_idx = {e: i for i, e in enumerate(NC_elements)}
    k = len(NC_elements)
    
    mult = [[0]*k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            mult[i][j] = NC_idx[NC_elements[i] * NC_elements[j]]
            
    NC_gens = NC.generators
    gen_indices = [NC_idx[g] for g in NC_gens]
    
    AutH_elements = list(AutH.elements)
    
    for target in product(AutH_elements, repeat=len(NC_gens)):
        mapping = {NC_idx[NC.identity]: AutH.identity}
        valid = True
        for i, g in enumerate(gen_indices):
            if g in mapping:
                if mapping[g] != target[i]:
                    valid = False
                    break
            else:
                mapping[g] = target[i]
                
        if not valid:
            continue
            
        queue = [NC_idx[NC.identity]]
        while queue and valid:
            curr = queue.pop(0)
            for i, g in enumerate(gen_indices):
                nxt = mult[curr][g]
                mapped_nxt = mapping[curr] * mapping[g]
                if nxt in mapping:
                    if mapping[nxt] != mapped_nxt:
                        valid = False
                        break
                else:
                    mapping[nxt] = mapped_nxt
                    queue.append(nxt)
                    
        if valid and len(mapping) == k:
            if len(set(mapping.values())) == k:
                return True
                
    return False

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, H, N, C = witness
            elif len(witness) == 2:
                G, H = witness
                N, C = None, None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        H_1 = H.is_subgroup(G)
    except Exception:
        H_1 = False
        
    try:
        N_true = get_normalizer(G, H)
        if len(witness) == 4:
            H_2 = N.is_subgroup(G) and set(N.elements) == set(N_true.elements)
        else:
            N = N_true
            H_2 = True
    except Exception:
        H_2 = False
        
    try:
        C_true = get_centralizer(G, H)
        if len(witness) == 4:
            H_3 = C.is_subgroup(G) and set(C.elements) == set(C_true.elements)
        else:
            C = C_true
            H_3 = True
    except Exception:
        H_3 = False
        
    try:
        if N is None or C is None:
            neg_Q = False
        else:
            Q = check_conclusion(G, H, N, C)
            neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [bool(H_1), bool(H_2), bool(H_3), bool(neg_Q)]