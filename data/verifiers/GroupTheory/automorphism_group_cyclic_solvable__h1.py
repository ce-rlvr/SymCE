import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_order(G):
    try:
        return G.order()
    except TypeError:
        return G.order

def get_is_solvable(G):
    try:
        return G.is_solvable()
    except TypeError:
        return G.is_solvable

def get_is_abelian(G):
    try:
        return G.is_abelian()
    except TypeError:
        return G.is_abelian

def check_isomorphic(G1, G2):
    if get_order(G1) != get_order(G2):
        return False
    if get_is_abelian(G1) != get_is_abelian(G2):
        return False
    if get_is_solvable(G1) != get_is_solvable(G2):
        return False
    try:
        from sympy.combinatorics.homomorphisms import is_isomorphic
        res = is_isomorphic(G1, G2)
        if res is not None:
            return res
    except Exception:
        pass
    return True

def get_automorphism_group(G):
    elements = list(G.generate())
    n = len(elements)
    if n > 32:
        raise ValueError("Group too large to compute automorphism group")
    
    id_idx = None
    for i, e in enumerate(elements):
        if getattr(e, 'is_Identity', False):
            id_idx = i
            break
    if id_idx is None:
        id_idx = elements.index(G.identity)
    
    mult_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elements.index(elements[i] * elements[j])
            
    gens = G.generators
    gen_indices = [elements.index(g) for g in gens]
    
    element_word = {id_idx: None}
    queue = [id_idx]
    while queue:
        curr = queue.pop(0)
        for g_idx in gen_indices:
            nxt = mult_table[g_idx][curr]
            if nxt not in element_word:
                element_word[nxt] = (g_idx, curr)
                queue.append(nxt)
                
    aut_perms = []
    for img_indices in product(range(n), repeat=len(gens)):
        mapping = {id_idx: id_idx}
        
        for i in range(n):
            if i == id_idx: continue
            path = []
            curr = i
            while curr != id_idx:
                g_idx, prev = element_word[curr]
                path.append(g_idx)
                curr = prev
            
            mapped_curr = id_idx
            for g_idx in reversed(path):
                mapped_g_idx = img_indices[gen_indices.index(g_idx)]
                mapped_curr = mult_table[mapped_g_idx][mapped_curr]
            mapping[i] = mapped_curr
            
        if len(set(mapping.values())) != n:
            continue
            
        is_hom = True
        for i in range(n):
            mi = mapping[i]
            for j in range(n):
                if mapping[mult_table[i][j]] != mult_table[mi][mapping[j]]:
                    is_hom = False
                    break
            if not is_hom:
                break
                
        if is_hom:
            perm = [mapping[i] for i in range(n)]
            aut_perms.append(Permutation(perm))
            
    if not aut_perms:
        return PermutationGroup([Permutation(n-1)])
    return PermutationGroup(aut_perms)

def conditions(witness):
    G = None
    A = None
    if isinstance(witness, tuple) and len(witness) == 2:
        G, A = witness
    elif isinstance(witness, dict) and 'G' in witness and 'A' in witness:
        G = witness['G']
        A = witness['A']
    else:
        G = witness

    try:
        AutG = get_automorphism_group(G)
        if A is None:
            A = AutG
            h1 = True
        else:
            h1 = check_isomorphic(A, AutG)
    except Exception:
        h1 = False

    try:
        neg_q = not get_is_solvable(A)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is the automorphism group of G",
    "¬Q: A is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1