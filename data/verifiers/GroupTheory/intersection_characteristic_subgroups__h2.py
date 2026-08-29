import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
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

def is_characteristic_set(G, H_elements):
    try:
        elements = list(G.generate())
        n = len(elements)
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        if not H_elements.issubset(set(elements)): 
            return False
        id_elem = G.identity
        if id_elem not in H_elements: 
            return False
        for h1 in H_elements:
            for h2 in H_elements:
                if h1 * h2 not in H_elements:
                    return False
        
        mult = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                mult[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        gens = G.generators
        gen_indices = [elem_to_idx[g] for g in gens]
        H_indices = {elem_to_idx[h] for h in H_elements}
        
        for target_gen_indices in itertools.product(range(n), repeat=len(gens)):
            mapping = {}
            for g_idx, tg_idx in zip(gen_indices, target_gen_indices):
                mapping[g_idx] = tg_idx
            id_idx = elem_to_idx[id_elem]
            mapping[id_idx] = id_idx
            
            queue = list(mapping.keys())
            head = 0
            valid = True
            while head < len(queue):
                u = queue[head]
                head += 1
                keys_to_check = list(mapping.keys())
                for v in keys_to_check:
                    uv = mult[u][v]
                    fu_fv = mult[mapping[u]][mapping[v]]
                    if uv in mapping:
                        if mapping[uv] != fu_fv:
                            valid = False
                            break
                    else:
                        mapping[uv] = fu_fv
                        queue.append(uv)
                    
                    vu = mult[v][u]
                    fv_fu = mult[mapping[v]][mapping[u]]
                    if vu in mapping:
                        if mapping[vu] != fv_fu:
                            valid = False
                            break
                    else:
                        mapping[vu] = fv_fu
                        queue.append(vu)
                if not valid:
                    break
            
            if valid and len(mapping) == n and len(set(mapping.values())) == n:
                H_img = {mapping[h] for h in H_indices}
                if H_img != H_indices:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, H_iterable = witness
        H_list = list(H_iterable)
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = True
        for H in H_list:
            if not isinstance(H, PermutationGroup):
                h2 = False
                break
            if not is_characteristic_set(G, set(list(H.generate()))):
                h2 = False
                break
    except Exception:
        h2 = False
        
    try:
        if not H_list:
            int_elements = set(list(G.generate()))
        else:
            int_elements = set.intersection(*[set(list(H.generate())) for H in H_list])
        neg_q = not is_characteristic_set(G, int_elements)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: For each i in I, H_i is a characteristic subgroup of G",
    "¬Q: The intersection of H_i is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2