import math
import itertools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def get_group_info(G):
    """
    Extracts the order, multiplication table, and identity index of a group.
    Handles integers (as cyclic groups Z_n) and SymPy PermutationGroups.
    """
    if isinstance(G, int) or (hasattr(G, 'is_Integer') and G.is_Integer):
        n = int(G)
        mult_table = [[(i + j) % n for j in range(n)] for i in range(n)]
        return n, mult_table, 0
        
    if hasattr(G, 'generate'):
        elements = list(G.generate())
    elif hasattr(G, 'elements'):
        elements = list(G.elements)
    else:
        elements = list(G)
        
    n = len(elements)
    id_idx = 0
    for i, e in enumerate(elements):
        if hasattr(e, 'is_Identity') and e.is_Identity:
            id_idx = i
            break
        try:
            if e * e == e:
                id_idx = i
                break
        except Exception:
            pass
            
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    mult_table = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
            
    return n, mult_table, id_idx

def get_direct_product_info(info_G, info_H):
    """
    Constructs the multiplication table for the direct product G x H.
    """
    n_G, table_G, id_G = info_G
    n_H, table_H, id_H = info_H
    n = n_G * n_H
    id_idx = id_G * n_H + id_H
    
    table = [[0] * n for _ in range(n)]
    for i_G in range(n_G):
        for i_H in range(n_H):
            i = i_G * n_H + i_H
            for j_G in range(n_G):
                for j_H in range(n_H):
                    j = j_G * n_H + j_H
                    k_G = table_G[i_G][j_G]
                    k_H = table_H[i_H][j_H]
                    k = k_G * n_H + k_H
                    table[i][j] = k
                    
    return n, table, id_idx

def count_automorphisms(n, mult_table, id_idx):
    """
    Counts the number of automorphisms of a finite group given its multiplication table.
    """
    if n <= 1:
        return 1
        
    # Find a generating set
    gens = []
    generated = {id_idx}
    for i in range(n):
        if i not in generated:
            gens.append(i)
            new_generated = set(generated)
            queue = list(generated)
            new_generated.add(i)
            queue.append(i)
            while queue:
                u = queue.pop(0)
                for g in gens:
                    v = mult_table[u][g]
                    if v not in new_generated:
                        new_generated.add(v)
                        queue.append(v)
            generated = new_generated
            if len(generated) == n:
                break
                
    # Precompute orders of all elements
    orders = [1] * n
    for i in range(n):
        if i == id_idx:
            continue
        curr = i
        k = 1
        while curr != id_idx:
            curr = mult_table[curr][i]
            k += 1
        orders[i] = k
        
    gen_orders = [orders[g] for g in gens]
    valid_targets = []
    for g_ord in gen_orders:
        valid_targets.append([i for i in range(n) if orders[i] == g_ord])
        
    aut_count = 0
    # Test all possible mappings of the generating set
    for targets in itertools.product(*valid_targets):
        mapping = {id_idx: id_idx}
        queue = [id_idx]
        is_valid = True
        
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            for i, g in enumerate(gens):
                v = mult_table[u][g]
                target_v = mult_table[mapping[u]][targets[i]]
                if v in mapping:
                    if mapping[v] != target_v:
                        is_valid = False
                        break
                else:
                    mapping[v] = target_v
                    queue.append(v)
            if not is_valid:
                break
                
        if is_valid and len(mapping) == n:
            aut_count += 1
            
    return aut_count

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: The greatest common divisor of the order of G and the order of H is 1
    try:
        info_G = get_group_info(G)
        info_H = get_group_info(H)
        order_G = info_G[0]
        order_H = info_H[0]
        h1 = (math.gcd(order_G, order_H) == 1)
    except Exception:
        h1 = False
        
    # neg_Q: The automorphism group of G x H is NOT isomorphic to Aut(G) x Aut(H)
    # We check this by comparing the sizes of the automorphism groups.
    try:
        aut_G = count_automorphisms(*info_G)
        aut_H = count_automorphisms(*info_H)
        info_GH = get_direct_product_info(info_G, info_H)
        aut_GH = count_automorphisms(*info_GH)
        
        neg_q = (aut_GH != aut_G * aut_H)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The greatest common divisor of the order of G and the order of H is 1",
    "¬Q: The automorphism group of G x H is NOT isomorphic to Aut(G) x Aut(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1