import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def precompute_words(n, gens_idx, table):
    parent = {0: None}
    gen_used = {0: None}
    queue = [0]
    head = 0
    while head < len(queue):
        curr = queue[head]
        head += 1
        for g in gens_idx:
            nxt = table[curr][g]
            if nxt not in parent:
                parent[nxt] = curr
                gen_used[nxt] = g
                queue.append(nxt)
    return parent, gen_used, queue

def is_complete(G):
    try:
        elements = list(G.generate())
        if len(elements) > 120:
            return None
            
        id_elem = None
        for e in elements:
            if e * e == e:
                id_elem = e
                break
                
        if id_elem is None:
            return None
            
        if elements[0] != id_elem:
            elements.remove(id_elem)
            elements.insert(0, id_elem)
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        n = len(elements)
        table = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                table[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        gens = G.generators
        gens_idx = [elem_to_idx[g] for g in gens]
        
        parent, gen_used, order = precompute_words(n, gens_idx, table)
        
        auts = []
        for target_idx in itertools.product(range(n), repeat=len(gens_idx)):
            p = {0: 0}
            gen_map = dict(zip(gens_idx, target_idx))
            
            valid = True
            for i in order:
                if i == 0: continue
                p_curr = p[parent[i]]
                p_g = gen_map[gen_used[i]]
                p_nxt = table[p_curr][p_g]
                p[i] = p_nxt
                
            if len(set(p.values())) != n:
                continue
                
            for i in range(n):
                if not valid: break
                for g in gens_idx:
                    if p[table[i][g]] != table[p[i]][p[g]]:
                        valid = False
                        break
            if valid:
                auts.append(tuple(p[i] for i in range(n)))
                
        m = len(auts)
        if m > 200:
            return None
            
        # Check if the center of Aut(G) is trivial
        center_A = []
        for a in auts:
            is_central = True
            for b in auts:
                for i in range(n):
                    if a[b[i]] != b[a[i]]:
                        is_central = False
                        break
                if not is_central:
                    break
            if is_central:
                center_A.append(a)
                
        if len(center_A) > 1:
            return False
            
        identity = tuple(range(n))
        if auts[0] != identity:
            auts.remove(identity)
            auts.insert(0, identity)
            
        # Find generators for Aut(G)
        A_gens = []
        A_elements = {identity}
        
        for a in auts:
            if a not in A_elements:
                A_gens.append(a)
                queue = list(A_elements)
                while queue:
                    curr = queue.pop(0)
                    for g in A_gens:
                        nxt = tuple(curr[g[i]] for i in range(n))
                        if nxt not in A_elements:
                            A_elements.add(nxt)
                            queue.append(nxt)
                if len(A_elements) == m:
                    break
                    
        A_elem_to_idx = {a: i for i, a in enumerate(auts)}
        A_table = [[0]*m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                a_i = auts[i]
                a_j = auts[j]
                prod = tuple(a_i[a_j[k]] for k in range(n))
                A_table[i][j] = A_elem_to_idx[prod]
                
        A_gens_idx = [A_elem_to_idx[g] for g in A_gens]
        A_parent, A_gen_used, A_order = precompute_words(m, A_gens_idx, A_table)
        
        # Compute the size of Aut(Aut(G))
        A_auts_count = 0
        for target_idx in itertools.product(range(m), repeat=len(A_gens_idx)):
            p = {0: 0}
            gen_map = dict(zip(A_gens_idx, target_idx))
            
            valid = True
            for i in A_order:
                if i == 0: continue
                p_curr = p[A_parent[i]]
                p_g = gen_map[A_gen_used[i]]
                p_nxt = A_table[p_curr][p_g]
                p[i] = p_nxt
                
            if len(set(p.values())) != m:
                continue
                
            for i in range(m):
                if not valid: break
                for g in A_gens_idx:
                    if p[A_table[i][g]] != A_table[p[i]][p[g]]:
                        valid = False
                        break
            if valid:
                A_auts_count += 1
                
        # Aut(G) is complete iff |Aut(Aut(G))| == |Aut(G)| (since its center is trivial)
        return A_auts_count == m
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        h1 = not witness.is_abelian
    except Exception:
        h1 = False
        
    try:
        comp = is_complete(witness)
        if comp is None:
            neg_q = False
        else:
            neg_q = not comp
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is non-abelian",
    "¬Q: The automorphism group Aut(G) is not a complete group"
]

N_HYP = 1
NEG_Q_INDEX = 1