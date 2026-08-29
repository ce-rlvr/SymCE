import math
import itertools
import functools
import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def are_isomorphic_fallback(G1, G2):
    if G1.order() != G2.order():
        return False
    if G1.is_abelian != G2.is_abelian:
        return False
    
    elems1 = list(G1.generate())
    elems2 = list(G2.generate())
    n = len(elems1)
    if n == 0: 
        return True
    
    idx1 = {e: i for i, e in enumerate(elems1)}
    idx2 = {e: i for i, e in enumerate(elems2)}
    
    t1 = [[idx1[a*b] for b in elems1] for a in elems1]
    t2 = [[idx2[a*b] for b in elems2] for a in elems2]
    
    id1 = idx1[G1.identity]
    id2 = idx2[G2.identity]
    
    def swap_id(t, id_idx):
        if id_idx == 0: 
            return t
        new_t = [row[:] for row in t]
        new_t[0], new_t[id_idx] = new_t[id_idx], new_t[0]
        for row in new_t:
            row[0], row[id_idx] = row[id_idx], row[0]
        for i in range(n):
            for j in range(n):
                if new_t[i][j] == 0: 
                    new_t[i][j] = id_idx
                elif new_t[i][j] == id_idx: 
                    new_t[i][j] = 0
        return new_t
        
    t1 = swap_id(t1, id1)
    t2 = swap_id(t2, id2)
    
    def get_orders(t):
        orders = []
        for i in range(n):
            curr = i
            o = 1
            while curr != 0:
                curr = t[curr][i]
                o += 1
                if o > n:
                    break
            orders.append(o)
        return orders
        
    ord1 = get_orders(t1)
    ord2 = get_orders(t2)
    if sorted(ord1) != sorted(ord2): 
        return False
    
    from collections import defaultdict
    by_ord1 = defaultdict(list)
    by_ord2 = defaultdict(list)
    for i, o in enumerate(ord1): 
        by_ord1[o].append(i)
    for i, o in enumerate(ord2): 
        by_ord2[o].append(i)
    
    keys = list(by_ord1.keys())
    
    def search(mapping, mapped_set, k_idx, l_idx):
        if k_idx == len(keys):
            for i in range(n):
                for j in range(n):
                    if mapping[t1[i][j]] != t2[mapping[i]][mapping[j]]:
                        return False
            return True
            
        k = keys[k_idx]
        l1 = by_ord1[k]
        l2 = by_ord2[k]
        
        if l_idx == len(l1):
            return search(mapping, mapped_set, k_idx + 1, 0)
            
        u = l1[l_idx]
        if u in mapping:
            return search(mapping, mapped_set, k_idx, l_idx + 1)
            
        for v in l2:
            if v not in mapped_set:
                ok = True
                for mu, mv in mapping.items():
                    if t1[u][mu] in mapping and mapping[t1[u][mu]] != t2[v][mv]:
                        ok = False
                        break
                    if t1[mu][u] in mapping and mapping[t1[mu][u]] != t2[mv][v]:
                        ok = False
                        break
                if ok:
                    mapping[u] = v
                    mapped_set.add(v)
                    if search(mapping, mapped_set, k_idx, l_idx + 1): 
                        return True
                    del mapping[u]
                    mapped_set.remove(v)
        return False
        
    return search({0: 0}, {0}, 0, 0)

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H1: N is a normal subgroup of G
    try:
        N_elements = set(N.generate())
        G_elements = set(G.generate())
        if not N_elements.issubset(G_elements):
            h1 = False
        else:
            h1 = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N_elements:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        H_elements = set(H.generate())
        h2 = H_elements.issubset(G_elements)
    except Exception:
        h2 = False

    # H3: G = NH
    try:
        NH_elements = set(n * h for n in N_elements for h in H_elements)
        h3 = (G_elements == NH_elements)
    except Exception:
        h3 = False

    # H4: N \cap H = {e}
    try:
        intersection = N_elements.intersection(H_elements)
        h4 = (len(intersection) == 1)
    except Exception:
        h4 = False

    # neg_Q: G/N is NOT isomorphic to H
    try:
        cosets = []
        seen = set()
        for g in G_elements:
            if g in seen:
                continue
            coset = frozenset(g * n for n in N_elements)
            cosets.append(coset)
            seen.update(coset)
            
        n_cosets = len(cosets)
        reps = [list(c)[0] for c in cosets]
        
        table = [[-1]*n_cosets for _ in range(n_cosets)]
        valid_table = True
        for i in range(n_cosets):
            for j in range(n_cosets):
                prod = reps[i] * reps[j]
                found = False
                for k, c in enumerate(cosets):
                    if prod in c:
                        table[i][j] = k
                        found = True
                        break
                if not found:
                    valid_table = False
                    break
            if not valid_table:
                break
                
        if not valid_table:
            neg_q = True
        else:
            perms = []
            for row in table:
                if sorted(row) != list(range(n_cosets)):
                    valid_table = False
                    break
                perms.append(Permutation(row))
                
            if not valid_table:
                neg_q = True
            else:
                G_mod_N = PermutationGroup(perms)
                if G_mod_N.order() != n_cosets:
                    neg_q = True
                else:
                    if hasattr(H, 'is_isomorphic'):
                        try:
                            neg_q = not H.is_isomorphic(G_mod_N)
                        except Exception:
                            neg_q = not are_isomorphic_fallback(H, G_mod_N)
                    else:
                        neg_q = not are_isomorphic_fallback(H, G_mod_N)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: G = NH",
    "H_4: N \\cap H = \\{e\\}",
    "¬Q: G/N is not isomorphic to H"
]

N_HYP = 4
NEG_Q_INDEX = 4