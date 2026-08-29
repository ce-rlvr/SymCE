import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation

# Top-level setup: named object bindings
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

def get_automorphism_group(G):
    elements = list(G.generate())
    n = len(elements)
    if n == 1:
        return PermutationGroup([Permutation(0)])
        
    identity = next(e for e in elements if e * e == e)
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    gens = G.generators
    gen_indices = [elem_to_idx[g] for g in gens]
    
    mult_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
            
    def get_closure(mapping):
        closure = mapping.copy()
        queue = list(mapping.keys())
        while queue:
            curr = queue.pop(0)
            keys = list(closure.keys())
            for k in keys:
                # curr * k
                prod1 = mult_table[curr][k]
                img_prod1 = mult_table[closure[curr]][closure[k]]
                if prod1 in closure:
                    if closure[prod1] != img_prod1:
                        return False
                else:
                    closure[prod1] = img_prod1
                    queue.append(prod1)
                
                # k * curr
                prod2 = mult_table[k][curr]
                img_prod2 = mult_table[closure[k]][closure[curr]]
                if prod2 in closure:
                    if closure[prod2] != img_prod2:
                        return False
                else:
                    closure[prod2] = img_prod2
                    queue.append(prod2)
        return closure

    automorphisms = []
    def search(gen_idx, current_mapping):
        if gen_idx == len(gen_indices):
            if len(current_mapping) == n and len(set(current_mapping.values())) == n:
                p = [current_mapping[i] for i in range(n)]
                automorphisms.append(Permutation(p))
            return
        
        g = gen_indices[gen_idx]
        if g in current_mapping:
            search(gen_idx + 1, current_mapping)
            return
            
        for img in range(n):
            new_mapping = current_mapping.copy()
            new_mapping[g] = img
            closure = get_closure(new_mapping)
            if closure is not False:
                search(gen_idx + 1, closure)
                
    search(0, {elem_to_idx[identity]: elem_to_idx[identity]})
    
    if not automorphisms:
        return PermutationGroup([Permutation(n-1)])
    return PermutationGroup(automorphisms)

def are_isomorphic(G, H):
    try:
        elements_G = list(G.generate())
        elements_H = list(H.generate())
    except Exception:
        return False
        
    if len(elements_G) != len(elements_H):
        return False
        
    n = len(elements_G)
    if n == 1:
        return True
        
    identity_G = next(e for e in elements_G if e * e == e)
    identity_H = next(e for e in elements_H if e * e == e)
    
    elem_to_idx_G = {e: i for i, e in enumerate(elements_G)}
    elem_to_idx_H = {e: i for i, e in enumerate(elements_H)}
    
    gens_G = G.generators
    gen_indices_G = [elem_to_idx_G[g] for g in gens_G]
    
    mult_table_G = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table_G[i][j] = elem_to_idx_G[elements_G[i] * elements_G[j]]
            
    mult_table_H = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table_H[i][j] = elem_to_idx_H[elements_H[i] * elements_H[j]]
            
    def get_closure(mapping):
        closure = mapping.copy()
        queue = list(mapping.keys())
        while queue:
            curr = queue.pop(0)
            keys = list(closure.keys())
            for k in keys:
                prod1 = mult_table_G[curr][k]
                img_prod1 = mult_table_H[closure[curr]][closure[k]]
                if prod1 in closure:
                    if closure[prod1] != img_prod1:
                        return False
                else:
                    closure[prod1] = img_prod1
                    queue.append(prod1)
                
                prod2 = mult_table_G[k][curr]
                img_prod2 = mult_table_H[closure[k]][closure[curr]]
                if prod2 in closure:
                    if closure[prod2] != img_prod2:
                        return False
                else:
                    closure[prod2] = img_prod2
                    queue.append(prod2)
        return closure

    def search(gen_idx, current_mapping):
        if gen_idx == len(gen_indices_G):
            if len(current_mapping) == n and len(set(current_mapping.values())) == n:
                return True
            return False
        
        g = gen_indices_G[gen_idx]
        if g in current_mapping:
            return search(gen_idx + 1, current_mapping)
            
        for img in range(n):
            new_mapping = current_mapping.copy()
            new_mapping[g] = img
            closure = get_closure(new_mapping)
            if closure is not False:
                if search(gen_idx + 1, closure):
                    return True
        return False
        
    return search(0, {elem_to_idx_G[identity_G]: elem_to_idx_H[identity_H]})

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # neg_Q: Aut(G) is NOT isomorphic to Aut(H)
    try:
        if not h1:
            neg_q = False
        else:
            aut_G = get_automorphism_group(G)
            aut_H = get_automorphism_group(H)
            neg_q = not are_isomorphic(aut_G, aut_H)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: Aut(G) is not isomorphic to Aut(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1