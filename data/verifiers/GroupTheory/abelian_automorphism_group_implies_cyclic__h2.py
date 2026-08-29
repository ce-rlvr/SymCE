import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    res = [False, False, False]
    
    try:
        res[0] = isinstance(witness, PermutationGroup) and witness.is_group and witness.order() < float('inf')
    except Exception:
        pass
        
    try:
        if res[0]:
            elements = list(witness.generate())
            n = len(elements)
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            
            mult = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    mult[i][j] = elem_to_idx[elements[i] * elements[j]]
                    
            gens = witness.generators
            gen_indices = [elem_to_idx[g] for g in gens]
            
            parent = [-1] * n
            edge = [-1] * n
            id_idx = elem_to_idx[witness.identity]
            
            queue = [id_idx]
            parent[id_idx] = id_idx
            
            head = 0
            while head < len(queue):
                curr = queue[head]
                head += 1
                for g_idx in gen_indices:
                    nxt = mult[curr][g_idx]
                    if parent[nxt] == -1:
                        parent[nxt] = curr
                        edge[nxt] = g_idx
                        queue.append(nxt)
                        
            automorphisms = []
            for img_tuple in itertools.product(range(n), repeat=len(gens)):
                gen_img = {g_idx: h_idx for g_idx, h_idx in zip(gen_indices, img_tuple)}
                
                mapping = [-1] * n
                mapping[id_idx] = id_idx
                
                for i in queue[1:]:
                    p = parent[i]
                    g = edge[i]
                    mapping[i] = mult[mapping[p]][gen_img[g]]
                    
                if len(set(mapping)) != n:
                    continue
                    
                is_homo = True
                for i in range(n):
                    for g_idx in gen_indices:
                        if mapping[mult[i][g_idx]] != mult[mapping[i]][gen_img[g_idx]]:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                        
                if is_homo:
                    automorphisms.append(mapping)
                    
            is_abelian = True
            for A in automorphisms:
                for B in automorphisms:
                    for g_idx in gen_indices:
                        if A[B[g_idx]] != B[A[g_idx]]:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
                if not is_abelian:
                    break
                    
            res[1] = is_abelian
    except Exception:
        pass
        
    try:
        res[2] = not witness.is_cyclic
    except Exception:
        pass
        
    return res

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The automorphism group of G is an abelian group",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2