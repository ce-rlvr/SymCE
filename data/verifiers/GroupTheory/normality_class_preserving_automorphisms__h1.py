import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from itertools import product

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

CONDITION_LABELS = [
    "H_1: Aut_c(G) is the set of all class-preserving automorphisms",
    "¬Q: Aut_c(G) is not a normal subgroup of Aut(G)"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G = witness
        if not hasattr(G, 'generate') or not hasattr(G, 'generators') or not hasattr(G, 'identity'):
            return [False, False]
            
        elements = list(G.generate())
        n = len(elements)
        if n == 0 or n > 256:  # Limit size to ensure fast execution
            return [False, False]
            
        gens = list(G.generators)
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        # Precompute multiplication table
        mult_table = [[0]*n for _ in range(n)]
        for i, e1 in enumerate(elements):
            for j, e2 in enumerate(elements):
                mult_table[i][j] = elem_to_idx[e1 * e2]
                
        id_idx = elem_to_idx[G.identity]
        
        # Precompute inverses
        inv_idx = [0]*n
        for i in range(n):
            for j in range(n):
                if mult_table[i][j] == id_idx:
                    inv_idx[i] = j
                    break
                    
        # Function to extend a mapping of generators to a full homomorphism
        def extend_mapping(gen_target_indices):
            mapping = {id_idx: id_idx}
            for i, g in enumerate(gens):
                mapping[elem_to_idx[g]] = gen_target_indices[i]
                
            queue = [id_idx]
            while queue:
                curr = queue.pop(0)
                for i, g in enumerate(gens):
                    g_idx = elem_to_idx[g]
                    nxt = mult_table[curr][g_idx]
                    target_nxt = mult_table[mapping[curr]][mapping[g_idx]]
                    if nxt not in mapping:
                        mapping[nxt] = target_nxt
                        queue.append(nxt)
                    else:
                        if mapping[nxt] != target_nxt:
                            return None
            if len(mapping) != n:
                return None
            # Check bijection
            if len(set(mapping.values())) != n:
                return None
            # Check full homomorphism property
            for i in range(n):
                for j in range(n):
                    if mapping[mult_table[i][j]] != mult_table[mapping[i]][mapping[j]]:
                        return None
            return tuple(mapping[i] for i in range(n))

        # Find all automorphisms of G
        auts = []
        for target_gens in product(range(n), repeat=len(gens)):
            mapping = extend_mapping(target_gens)
            if mapping is not None:
                auts.append(mapping)
                
        # Precompute conjugacy classes
        conj_classes = []
        for x in range(n):
            cls = set()
            for g in range(n):
                gx = mult_table[g][x]
                gxg_inv = mult_table[gx][inv_idx[g]]
                cls.add(gxg_inv)
            conj_classes.append(cls)
            
        # Find Aut_c(G): the set of all class-preserving automorphisms
        aut_c = []
        for aut in auts:
            is_cp = True
            for x in range(n):
                if aut[x] not in conj_classes[x]:
                    is_cp = False
                    break
            if is_cp:
                aut_c.append(aut)
                
        N_set = set(aut_c)
        is_normal = True
        
        # 1. Check Identity
        id_aut = tuple(range(n))
        if id_aut not in N_set:
            is_normal = False
            
        # 2. Check Closure
        if is_normal:
            for n1 in aut_c:
                for n2 in aut_c:
                    comp = tuple(n1[n2[x]] for x in range(n))
                    if comp not in N_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        # 3. Check Inverses
        if is_normal:
            for n1 in aut_c:
                inv = [0]*n
                for x in range(n):
                    inv[n1[x]] = x
                if tuple(inv) not in N_set:
                    is_normal = False
                    break
                    
        # 4. Check Normality (g * n * g^-1 in N for all g in Aut(G), n in Aut_c(G))
        if is_normal:
            for n1 in aut_c:
                for g in auts:
                    g_inv = [0]*n
                    for x in range(n):
                        g_inv[g[x]] = x
                    comp = tuple(g[n1[g_inv[x]]] for x in range(n))
                    if comp not in N_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        H1_ok = True
        neg_Q_ok = not is_normal
        
        return [H1_ok, neg_Q_ok]
    except Exception:
        return [False, False]