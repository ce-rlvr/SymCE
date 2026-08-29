import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from itertools import product

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

def conditions(witness) -> list[bool]:
    try:
        # H_1: G is a group
        if not isinstance(witness, PermutationGroup):
            return [False, False, False]
        h1 = True
    except Exception:
        return [False, False, False]
        
    try:
        # H_2: Inn(G) is the group of inner automorphisms of G
        # This is a definitional hypothesis that holds for any valid group.
        h2 = True
    except Exception:
        h2 = False
        
    try:
        # Compute elements and multiplication table
        elements = list(witness.generate())
        n = len(elements)
        idx = {g: i for i, g in enumerate(elements)}
        gens = witness.generators
        gen_indices = [idx[g] for g in gens]
        
        mult = [[idx[g*h] for h in elements] for g in elements]
        
        # Precompute orders to prune the search space for automorphisms
        orders = [g.order() for g in elements]
        gen_orders = [orders[gi] for gi in gen_indices]
        
        # Find all automorphisms of G
        auts = []
        for img in product(range(n), repeat=len(gens)):
            # An automorphism must map generators to elements of the same order
            if any(orders[img[i]] != gen_orders[i] for i in range(len(gens))):
                continue
                
            mapping = {idx[witness.identity]: idx[witness.identity]}
            consistent = True
            for i, gi in enumerate(gen_indices):
                if gi in mapping and mapping[gi] != img[i]:
                    consistent = False
                    break
                mapping[gi] = img[i]
                
            if not consistent:
                continue
                
            # BFS to generate the full mapping
            queue = [idx[witness.identity]]
            head = 0
            while head < len(queue):
                u = queue[head]
                head += 1
                for gi in gen_indices:
                    v = mult[u][gi]
                    mapped_v = mult[mapping[u]][mapping[gi]]
                    if v in mapping:
                        if mapping[v] != mapped_v:
                            consistent = False
                            break
                    else:
                        mapping[v] = mapped_v
                        queue.append(v)
                if not consistent:
                    break
                    
            if consistent and len(mapping) == n:
                if len(set(mapping.values())) == n:
                    aut = tuple(mapping[i] for i in range(n))
                    auts.append(aut)
                    
        # Find all inner automorphisms of G
        inn_auts = []
        for x in range(n):
            x_inv = idx[elements[x]**-1]
            # gamma_x(g) = x * g * x^-1
            aut = tuple(mult[mult[x][g]][x_inv] for g in range(n))
            inn_auts.append(aut)
        inn_auts_set = set(inn_auts)
        
        # Compute the centralizer of Inn(G) in Aut(G)
        C_Aut_Inn = set()
        for alpha in auts:
            commutes = True
            for iota in inn_auts_set:
                for g in range(n):
                    if alpha[iota[g]] != iota[alpha[g]]:
                        commutes = False
                        break
                if not commutes:
                    break
            if commutes:
                C_Aut_Inn.add(alpha)
                
        # Compute the center of G, Z(G)
        Z_G = set()
        for i in range(n):
            is_central = True
            for j in range(n):
                if mult[i][j] != mult[j][i]:
                    is_central = False
                    break
            if is_central:
                Z_G.add(i)
                
        # Compute the group of central automorphisms of G
        # A central automorphism is an alpha in Aut(G) such that g^-1 * alpha(g) in Z(G) for all g in G
        Cent_Aut = set()
        for alpha in auts:
            is_cent = True
            for g in range(n):
                g_inv = idx[elements[g]**-1]
                val = mult[g_inv][alpha[g]]
                if val not in Z_G:
                    is_cent = False
                    break
            if is_cent:
                Cent_Aut.add(alpha)
                
        # ¬Q: The centralizer of Inn(G) in Aut(G) is NOT the group of central automorphisms of G
        neg_q = bool(C_Aut_Inn != Cent_Aut)
        
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: The centralizer of Inn(G) in Aut(G) is not the group of central automorphisms of G"
]

N_HYP = 2
NEG_Q_INDEX = 2