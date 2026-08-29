import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import product

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_characteristic(G, H):
    elements = list(G.generate())
    n = len(elements)
    if n > 100:
        return False
        
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    mult = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult[i][j] = elem_to_idx[elements[i] * elements[j]]
            
    gens = G.generators
    gen_indices = [elem_to_idx[g] for g in gens]
    
    try:
        H_elements = list(H.generate())
        H_indices = set(elem_to_idx[h] for h in H_elements)
    except KeyError:
        return False
        
    for img_indices in product(range(n), repeat=len(gens)):
        gen_map = dict(zip(gen_indices, img_indices))
        
        mapping = {elem_to_idx[G.identity]: elem_to_idx[G.identity]}
        queue = [elem_to_idx[G.identity]]
        head = 0
        valid = True
        
        while head < len(queue):
            u = queue[head]
            head += 1
            for g_idx in gen_indices:
                v = mult[u][g_idx]
                mapped_v = mult[mapping[u]][gen_map[g_idx]]
                if v in mapping:
                    if mapping[v] != mapped_v:
                        valid = False
                        break
                else:
                    mapping[v] = mapped_v
                    queue.append(v)
            if not valid:
                break
                
        if valid and len(mapping) == n:
            if len(set(mapping.values())) == n:
                mapped_H = set(mapping[h_idx] for h_idx in H_indices)
                if mapped_H != H_indices:
                    return False
                    
    return True

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # neg_Q: H is not a characteristic subgroup of G
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = True
        else:
            try:
                is_sub = H.is_subgroup(G)
            except Exception:
                is_sub = False
                
            if not is_sub:
                neg_q = True
            else:
                neg_q = not is_characteristic(G, H)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1