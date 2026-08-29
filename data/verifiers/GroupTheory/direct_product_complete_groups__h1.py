import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def count_automorphisms(G):
    elements = list(G.elements)
    n = len(elements)
    gens = list(G.generators)
    
    identity = None
    for e in elements:
        if e * e == e:
            identity = e
            break
            
    elem_to_idx = {identity: 0}
    idx_to_elem = [identity]
    
    tree = [(None, None)]
    
    queue = [0]
    while queue:
        curr_idx = queue.pop(0)
        curr_elem = idx_to_elem[curr_idx]
        
        for i, gen in enumerate(gens):
            next_elem = curr_elem * gen
            if next_elem not in elem_to_idx:
                next_idx = len(idx_to_elem)
                elem_to_idx[next_elem] = next_idx
                idx_to_elem.append(next_elem)
                tree.append((curr_idx, i))
                queue.append(next_idx)
                
    conditions_list = []
    for u, u_elem in enumerate(idx_to_elem):
        for i, gen in enumerate(gens):
            v_elem = u_elem * gen
            v = elem_to_idx[v_elem]
            conditions_list.append((u, i, v))
            
    def perm_order(p):
        if p * p == p:
            return 1
        p_pow = p
        o = 1
        while p_pow * p_pow != p_pow:
            p_pow = p_pow * p
            o += 1
        return o

    orders = {g: perm_order(g) for g in gens}
    candidates = []
    for gen in gens:
        o = orders[gen]
        cands = [h for h in elements if perm_order(h) == o]
        candidates.append(cands)
        
    aut_count = 0
    for mapped_gens in itertools.product(*candidates):
        mapped_elements = [None] * n
        mapped_elements[0] = identity
        
        for i in range(1, n):
            p_idx, gen_idx = tree[i]
            mapped_elements[i] = mapped_elements[p_idx] * mapped_gens[gen_idx]
            
        if len(set(mapped_elements)) != n:
            continue
            
        valid = True
        for u, i, v in conditions_list:
            if mapped_elements[u] * mapped_gens[i] != mapped_elements[v]:
                valid = False
                break
                
        if valid:
            aut_count += 1
            
    return aut_count

def is_complete(G):
    elements = list(G.elements)
    n = len(elements)
    if n <= 1:
        return False
        
    C = G.center()
    if len(list(C.elements)) > 1:
        return False
        
    aut_count = count_automorphisms(G)
    return aut_count == n

def direct_product(G, H):
    m = G.degree
    n = H.degree
    
    new_gens = []
    for g in G.generators:
        arr = list(g.array_form)
        arr = arr + list(range(len(arr), m))
        arr = arr + list(range(m, m + n))
        new_gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(h.array_form)
        arr = arr + list(range(len(arr), n))
        new_arr = list(range(m)) + [x + m for x in arr]
        new_gens.append(Permutation(new_arr))
        
    return PermutationGroup(new_gens)

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_complete(G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_complete(H)
    except Exception:
        h2 = False
        
    try:
        GxH = direct_product(G, H)
        neg_q = not is_complete(GxH)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a complete group",
    "H_2: H is a complete group",
    "¬Q: G \\times H is not a complete group"
]

N_HYP = 2
NEG_Q_INDEX = 2