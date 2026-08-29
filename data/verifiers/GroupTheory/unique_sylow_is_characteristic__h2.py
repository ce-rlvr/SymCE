import itertools
import math
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def is_characteristic(G, P):
    elements = list(G.generate())
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    n = len(elements)
    
    mult_table = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
            
    gens = G.generators
    gen_indices = [elem_to_idx[g] for g in gens]
    P_indices = {elem_to_idx[e] for e in P.generate()}
    
    id_idx = elem_to_idx[G.identity]
    
    tree_edges = []
    visited = {id_idx}
    q = [id_idx]
    while q:
        curr = q.pop(0)
        for g_idx in gen_indices:
            nxt = mult_table[curr][g_idx]
            if nxt not in visited:
                visited.add(nxt)
                tree_edges.append((curr, g_idx, nxt))
                q.append(nxt)
                
    gen_orders = [g.order() for g in gens]
    elem_orders = [e.order() for e in elements]
    
    valid_targets = []
    for g_ord in gen_orders:
        targets = [i for i, e_ord in enumerate(elem_orders) if e_ord == g_ord]
        valid_targets.append(targets)
        
    for target_gens in itertools.product(*valid_targets):
        phi = {id_idx: id_idx}
        for g_idx, t_idx in zip(gen_indices, target_gens):
            phi[g_idx] = t_idx
            
        for u, g_idx, v in tree_edges:
            phi[v] = mult_table[phi[u]][phi[g_idx]]
            
        if len(set(phi.values())) != n:
            continue
            
        is_homo = True
        for i in range(n):
            phi_i = phi[i]
            row_i = mult_table[i]
            row_phi_i = mult_table[phi_i]
            for j in range(n):
                if phi[row_i[j]] != row_phi_i[phi[j]]:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        if is_homo:
            P_img = {phi[p] for p in P_indices}
            if P_img != P_indices:
                return False
                
    return True

def conditions(witness) -> list[bool]:
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if not isinstance(P, PermutationGroup):
            h2 = False
        elif not P.is_subgroup(G):
            h2 = False
        elif not sympy.isprime(p):
            h2 = False
        else:
            order_P = P.order()
            order_G = G.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            h2 = (order_P == p**k)
    except Exception:
        h2 = False
        
    try:
        if not h2:
            h3 = False
        else:
            h3 = P.is_normal(G)
    except Exception:
        h3 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            neg_q = not is_characteristic(G, P)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: P is the unique Sylow p-subgroup of G for the prime p",
    "¬Q: P is not a characteristic subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3