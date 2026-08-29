import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import DirectProduct

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, p, k = witness
                pairs = [(p, k)]
            elif len(witness) == 2:
                G, p = witness
                if not hasattr(G, 'order'):
                    return [False, False]
                n = int(G.order())
                pairs = []
                k = 2
                while p**k <= n:
                    if p**k == n:
                        pairs.append((p, k))
                    k += 1
            else:
                return [False, False]
        else:
            G = witness
            if not hasattr(G, 'order'):
                return [False, False]
            n = int(G.order())
            pairs = []
            for p in range(2, int(math.isqrt(n)) + 1):
                k = 2
                while p**k <= n:
                    if p**k == n:
                        pairs.append((p, k))
                    k += 1
                    
        if not pairs:
            return [False, False]
            
        h1_ok = True
        
        # Generate group elements and multiplication table
        elements = list(G.generate())
        n_elems = len(elements)
        if n_elems > 1024:  # Protect against excessively large groups
            return [False, False]
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        mul_table = [[0] * n_elems for _ in range(n_elems)]
        for i in range(n_elems):
            for j in range(n_elems):
                mul_table[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        gens = G.generators
        gen_indices = [elem_to_idx[g] for g in gens]
        orders = [e.order() for e in elements]
        
        cands_by_order = {}
        for i, o in enumerate(orders):
            cands_by_order.setdefault(o, []).append(i)
            
        automorphisms = []
        id_idx = elem_to_idx[G.identity]
        step_count = [0]
        
        # Backtracking search to find all automorphisms
        def search(gen_idx, mapping, queue_start):
            if step_count[0] > 200000:
                raise TimeoutError("Too many steps in automorphism search")
            step_count[0] += 1
            
            keys = list(mapping.keys())
            head = queue_start
            
            # Propagate closure to ensure mapping is a valid homomorphism
            while head < len(keys):
                u = keys[head]
                head += 1
                for i in range(gen_idx):
                    g_i = gen_indices[i]
                    
                    # Right multiplication
                    v = mul_table[u][g_i]
                    mapped_v = mul_table[mapping[u]][mapping[g_i]]
                    if v in mapping:
                        if mapping[v] != mapped_v:
                            return
                    else:
                        mapping[v] = mapped_v
                        keys.append(v)
                        
                    # Left multiplication
                    v2 = mul_table[g_i][u]
                    mapped_v2 = mul_table[mapping[g_i]][mapping[u]]
                    if v2 in mapping:
                        if mapping[v2] != mapped_v2:
                            return
                    else:
                        mapping[v2] = mapped_v2
                        keys.append(v2)
                        
            if gen_idx == len(gens):
                if len(mapping) == n_elems and len(set(mapping.values())) == n_elems:
                    automorphisms.append(tuple(mapping[i] for i in range(n_elems)))
                return
                
            g = gen_indices[gen_idx]
            if g in mapping:
                search(gen_idx + 1, mapping.copy(), head)
                return
                
            g_order = orders[g]
            for cand in cands_by_order.get(g_order, []):
                if cand in mapping.values():
                    continue
                new_mapping = mapping.copy()
                new_mapping[g] = cand
                search(gen_idx + 1, new_mapping, head)
                
        search(0, {id_idx: id_idx}, 0)
        
        # Compute inner automorphisms
        inner_automorphisms = set()
        for g_idx in range(n_elems):
            g_inv_idx = None
            for h_idx in range(n_elems):
                if mul_table[g_idx][h_idx] == id_idx:
                    g_inv_idx = h_idx
                    break
            
            mapping = []
            for x_idx in range(n_elems):
                gx = mul_table[g_idx][x_idx]
                gxg = mul_table[gx][g_inv_idx]
                mapping.append(gxg)
            inner_automorphisms.add(tuple(mapping))
            
        # Compute order of each automorphism in Out(G) = Aut(G) / Inn(G)
        def order_in_out(f):
            current = f
            m = 1
            while current not in inner_automorphisms:
                current = tuple(f[current[i]] for i in range(n_elems))
                m += 1
            return m
            
        out_orders = set()
        for f in automorphisms:
            out_orders.add(order_in_out(f))
            
        # Check if Out(G) lacks an element of order p for ANY valid (p, k)
        neg_q_ok = False
        for p, k in pairs:
            if p not in out_orders:
                neg_q_ok = True
                break
                
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group of order p^k for some integer k >= 2",
    "¬Q: Out(G) does not contain an element of order p"
]

N_HYP = 1
NEG_Q_INDEX = 1