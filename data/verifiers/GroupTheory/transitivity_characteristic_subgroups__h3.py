import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(G):
    return isinstance(G, PermutationGroup)

def is_characteristic(G, H):
    if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
        return False
        
    try:
        def perm_to_tuple(p):
            arr = list(p.array_form)
            while arr and arr[-1] == len(arr) - 1:
                arr.pop()
            return tuple(arr)

        elements = list(G.generate())
        n = len(elements)
        gens = G.generators
        
        elem_to_idx = {perm_to_tuple(e): i for i, e in enumerate(elements)}
        
        H_elements = list(H.generate())
        H_idx = set()
        for e in H_elements:
            pt = perm_to_tuple(e)
            if pt not in elem_to_idx:
                return False
            H_idx.add(elem_to_idx[pt])
            
        mult = [[0]*n for _ in range(n)]
        for i, e1 in enumerate(elements):
            for j, e2 in enumerate(elements):
                mult[i][j] = elem_to_idx[perm_to_tuple(e1 * e2)]
                
        gen_idx = [elem_to_idx[perm_to_tuple(g)] for g in gens]
        id_idx = elem_to_idx[perm_to_tuple(G.identity)]
        
        for target in itertools.product(range(n), repeat=len(gens)):
            target_idx = target
            
            q = [id_idx]
            visited_tree = {id_idx}
            bfs_order = [id_idx]
            parent = {}
            
            while q:
                curr = q.pop(0)
                for i, g_i in enumerate(gen_idx):
                    nxt = mult[curr][g_i]
                    if nxt not in visited_tree:
                        visited_tree.add(nxt)
                        parent[nxt] = (curr, i)
                        bfs_order.append(nxt)
                        q.append(nxt)
                        
            f_full = {id_idx: id_idx}
            for node in bfs_order:
                if node == id_idx:
                    continue
                p, g_idx_used = parent[node]
                f_full[node] = mult[f_full[p]][target_idx[g_idx_used]]
                
            if len(set(f_full.values())) != n:
                continue
                
            is_homo = True
            for x in range(n):
                for y in range(n):
                    if f_full[mult[x][y]] != mult[f_full[x]][f_full[y]]:
                        is_homo = False
                        break
                if not is_homo:
                    break
                    
            if is_homo:
                mapped_H = {f_full[h] for h in H_idx}
                if mapped_H != H_idx:
                    return False
                    
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_characteristic(G, H)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_characteristic(G, K)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a characteristic subgroup of G",
    "¬Q: K is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2