import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools

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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def count_automorphisms(N):
    elements = list(N.generate())
    n = len(elements)
    if n == 1:
        return 1
    idx = {e: i for i, e in enumerate(elements)}
    mult = [[idx[e1 * e2] for e2 in elements] for e1 in elements]
    
    gens = N.generators
    gen_indices = [idx[g] for g in gens]
    
    aut_count = 0
    for img_gen_indices in itertools.product(range(n), repeat=len(gens)):
        closure = set(img_gen_indices)
        closure.add(idx[N.identity])
        queue = list(closure)
        while queue:
            curr = queue.pop(0)
            for g in img_gen_indices:
                nxt = mult[curr][g]
                if nxt not in closure:
                    closure.add(nxt)
                    queue.append(nxt)
        if len(closure) != n:
            continue
            
        f = [-1] * n
        f[idx[N.identity]] = idx[N.identity]
        valid_init = True
        for g_idx, img_idx in zip(gen_indices, img_gen_indices):
            if f[g_idx] != -1 and f[g_idx] != img_idx:
                valid_init = False
                break
            f[g_idx] = img_idx
            
        if not valid_init:
            continue
            
        queue = [idx[N.identity]]
        valid = True
        while queue:
            curr = queue.pop(0)
            for g_idx in gen_indices:
                nxt = mult[curr][g_idx]
                expected_img = mult[f[curr]][f[g_idx]]
                if f[nxt] == -1:
                    f[nxt] = expected_img
                    queue.append(nxt)
                elif f[nxt] != expected_img:
                    valid = False
                    break
            if not valid:
                break
                
        if valid:
            aut_count += 1
            
    return aut_count

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group and N is a subgroup of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
        if h1:
            for g in N.generators:
                if g not in G:
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # H2: The center of N is trivial
    try:
        if not h1:
            h2 = False
        else:
            try:
                c_order = N.center().order()
            except Exception:
                n_gens = N.generators
                c_order = sum(1 for g in N.generate() if all(g * x == x * g for x in n_gens))
            h2 = (c_order == 1)
    except Exception:
        h2 = False
        
    # H3: Every automorphism of N is an inner automorphism
    try:
        if not h1 or not h2:
            h3 = False
        else:
            try:
                n = N.order()
            except Exception:
                n = len(list(N.generate()))
                
            if n > 100:
                h3 = False
            else:
                h3 = (count_automorphisms(N) == n)
    except Exception:
        h3 = False
        
    # neg_Q: G is NOT isomorphic to N \times C_G(N)
    try:
        if not h1:
            neg_q = False
        else:
            N_gens = N.generators
            C_elements = []
            for g in G.generate():
                if all(g * n == n * g for n in N_gens):
                    C_elements.append(g)
            
            c_order = len(C_elements)
            
            try:
                g_order = G.order()
            except Exception:
                g_order = len(list(G.generate()))
                
            try:
                n_order = N.order()
            except Exception:
                n_order = len(list(N.generate()))
            
            if g_order != n_order * c_order:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "H_2: The center of N is trivial",
    "H_3: Every automorphism of N is an inner automorphism",
    "¬Q: G is not isomorphic to the direct product N \\times C_G(N)"
]

N_HYP = 3
NEG_Q_INDEX = 3