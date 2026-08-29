import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        is_group = isinstance(witness, PermutationGroup)
    except Exception:
        is_group = False

    if not is_group:
        return [False, False, False]

    # H2: Aut(G) is the automorphism group of G (definitional hypothesis)
    h2 = True

    try:
        elements = list(witness.elements)
        n = len(elements)
        if n == 0:
            return [is_group, h2, False]
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        # Build multiplication table
        mult = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                mult[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        # Find identity element index
        id_idx = None
        for i in range(n):
            if mult[i][i] == i:
                id_idx = i
                break
                
        gens = witness.generators
        gen_indices = [elem_to_idx[g] for g in gens]
        
        # Find all automorphisms of G
        auts = []
        for target in product(range(n), repeat=len(gens)):
            mapping = {id_idx: id_idx}
            valid = True
            
            for g_idx, t_idx in zip(gen_indices, target):
                if g_idx in mapping:
                    if mapping[g_idx] != t_idx:
                        valid = False
                        break
                else:
                    mapping[g_idx] = t_idx
                    
            if not valid:
                continue
                
            queue = list(mapping.items())
            head = 0
            while head < len(queue) and valid:
                u, fu = queue[head]
                head += 1
                for g_idx, t_idx in zip(gen_indices, target):
                    v = mult[u][g_idx]
                    fv = mult[fu][t_idx]
                    if v in mapping:
                        if mapping[v] != fv:
                            valid = False
                            break
                    else:
                        mapping[v] = fv
                        queue.append((v, fv))
                        
            if valid and len(mapping) == n and len(set(mapping.values())) == n:
                aut = tuple(mapping[i] for i in range(n))
                auts.append(aut)
                
        # Find Inn(G)
        inn_auts = set()
        for x_idx in range(n):
            x_inv_idx = None
            for y_idx in range(n):
                if mult[x_idx][y_idx] == id_idx:
                    x_inv_idx = y_idx
                    break
            
            gamma_x = []
            for g_idx in range(n):
                xg = mult[x_idx][g_idx]
                xgx_inv = mult[xg][x_inv_idx]
                gamma_x.append(xgx_inv)
            inn_auts.add(tuple(gamma_x))
            
        # Find Centralizer of Inn(G) in Aut(G)
        centralizer = set()
        for aut in auts:
            is_centralizer = True
            for gamma in inn_auts:
                for g_idx in range(n):
                    if aut[gamma[g_idx]] != gamma[aut[g_idx]]:
                        is_centralizer = False
                        break
                if not is_centralizer:
                    break
            if is_centralizer:
                centralizer.add(aut)
                
        # Find Z(G)
        Z_G = set()
        for i in range(n):
            is_center = True
            for j in range(n):
                if mult[i][j] != mult[j][i]:
                    is_center = False
                    break
            if is_center:
                Z_G.add(i)
                
        # Find group of central automorphisms of G
        central_auts = set()
        for aut in auts:
            is_central = True
            for g_idx in range(n):
                g_inv_idx = None
                for y_idx in range(n):
                    if mult[g_idx][y_idx] == id_idx:
                        g_inv_idx = y_idx
                        break
                
                val = mult[g_inv_idx][aut[g_idx]]
                if val not in Z_G:
                    is_central = False
                    break
            if is_central:
                central_auts.add(aut)
                
        # Negated conclusion: The centralizer of Inn(G) in Aut(G) is NOT the group of central automorphisms
        neg_q = (centralizer != central_auts)
        
        return [is_group, h2, neg_q]
        
    except Exception:
        return [is_group, h2, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Aut(G) is the automorphism group of G",
    "¬Q: The centralizer of Inn(G) in Aut(G) is not the group of central automorphisms of G"
]

N_HYP = 2
NEG_Q_INDEX = 2