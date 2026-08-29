import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def check_aut_c_normal(G):
    try:
        elements = list(G.generate())
    except AttributeError:
        return False
        
    n = len(elements)
    if n > 256:
        return False
        
    elem_idx = {e: i for i, e in enumerate(elements)}
    mult = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult[i][j] = elem_idx[elements[i] * elements[j]]
            
    id_idx = elem_idx[G.identity]
    
    gens = list(G.generators)
    gen_indices = [elem_idx[g] for g in gens]
    
    orders = [0]*n
    for i in range(n):
        curr = i
        ord_i = 1
        while curr != id_idx:
            curr = mult[curr][i]
            ord_i += 1
        orders[i] = ord_i
        
    gen_orders = [orders[i] for i in gen_indices]
    
    valid_targets = []
    for go in gen_orders:
        valid_targets.append([i for i in range(n) if orders[i] == go])
        
    automorphisms = []
    
    def extend_hom_full(current_mapping):
        mapping = current_mapping.copy()
        queue = list(mapping.keys())
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            for v in range(head):
                v_idx = queue[v]
                
                uv = mult[u][v_idx]
                mapped_uv = mult[mapping[u]][mapping[v_idx]]
                if uv in mapping:
                    if mapping[uv] != mapped_uv:
                        return None
                else:
                    mapping[uv] = mapped_uv
                    queue.append(uv)
                
                if u != v_idx:
                    vu = mult[v_idx][u]
                    mapped_vu = mult[mapping[v_idx]][mapping[u]]
                    if vu in mapping:
                        if mapping[vu] != mapped_vu:
                            return None
                    else:
                        mapping[vu] = mapped_vu
                        queue.append(vu)
                        
        if len(mapping) == n:
            return mapping
        return None

    def search(gen_idx, current_mapping):
        if len(automorphisms) > 500000:
            return
            
        if gen_idx == len(gen_indices):
            mapping = extend_hom_full(current_mapping)
            if mapping is not None and len(set(mapping.values())) == n:
                aut_tuple = tuple(mapping[i] for i in range(n))
                automorphisms.append(aut_tuple)
            return
            
        g = gen_indices[gen_idx]
        if g in current_mapping:
            search(gen_idx + 1, current_mapping)
            return
            
        for t in valid_targets[gen_idx]:
            possible = True
            for prev_g, prev_t in current_mapping.items():
                prod_g = mult[g][prev_g]
                prod_t = mult[t][prev_t]
                if orders[prod_g] != orders[prod_t]:
                    possible = False
                    break
                prod_g2 = mult[prev_g][g]
                prod_t2 = mult[prev_t][t]
                if orders[prod_g2] != orders[prod_t2]:
                    possible = False
                    break
            if not possible:
                continue
                
            new_mapping = current_mapping.copy()
            new_mapping[g] = t
            search(gen_idx + 1, new_mapping)

    search(0, {id_idx: id_idx})
    
    Z_set = set()
    for i in range(n):
        is_central = True
        for j in range(n):
            if mult[i][j] != mult[j][i]:
                is_central = False
                break
        if is_central:
            Z_set.add(i)
            
    inv = [0]*n
    for i in range(n):
        for j in range(n):
            if mult[i][j] == id_idx:
                inv[i] = j
                break
                
    Aut_c = []
    for alpha in automorphisms:
        is_cent = True
        for i in range(n):
            if mult[inv[i]][alpha[i]] not in Z_set:
                is_cent = False
                break
        if is_cent:
            Aut_c.append(alpha)
            
    Aut_c_set = set(Aut_c)
    
    for alpha in Aut_c:
        for beta in automorphisms:
            conj = [0]*n
            for i in range(n):
                conj[beta[i]] = beta[alpha[i]]
            if tuple(conj) not in Aut_c_set:
                return True
                
    return False

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = check_aut_c_normal(witness)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: Aut_c(G) is not a normal subgroup of Aut(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1