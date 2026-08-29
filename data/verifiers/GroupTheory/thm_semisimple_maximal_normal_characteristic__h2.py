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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
trivial = CyclicGroup(1)

def get_automorphism_mapping(G, gens, img_gens):
    mapping = {G.identity: G.identity}
    queue = [G.identity]
    
    idx = 0
    while idx < len(queue):
        curr = queue[idx]
        idx += 1
        for g, ig in zip(gens, img_gens):
            nxt = curr * g
            nxt_img = mapping[curr] * ig
            if nxt in mapping:
                if mapping[nxt] != nxt_img:
                    return None
            else:
                mapping[nxt] = nxt_img
                queue.append(nxt)
                
    if len(set(mapping.values())) != G.order():
        return None
        
    return mapping

def is_characteristic(G, N):
    if not G.is_normal(N):
        return False
        
    gens = G.generators
    elements = list(G.elements)
    
    valid_images = []
    for g in gens:
        valid_images.append([e for e in elements if e.order() == g.order()])
        
    for img_gens in product(*valid_images):
        mapping = get_automorphism_mapping(G, gens, img_gens)
        if mapping is not None:
            for n in N.generators:
                if mapping[n] not in N:
                    return False
    return True

def strictly_contains(H, N):
    if H.order() <= N.order():
        return False
    for g in N.generators:
        if g not in H:
            return False
    return True

def is_semisimple(H):
    if H.order() == 1:
        return True
    # The smallest non-abelian simple group is A5 (order 60).
    if H.order() < 60:
        return False
    if H.derived_subgroup().order() != H.order():
        return False
        
    def is_ab(grp):
        if hasattr(grp, 'is_abelian'):
            return grp.is_abelian
        return grp.derived_subgroup().order() == 1

    if hasattr(H, 'normal_subgroups'):
        for N_sub in H.normal_subgroups():
            if N_sub.order() > 1 and is_ab(N_sub):
                return False
    elif hasattr(H, 'subgroups'):
        for N_sub in H.subgroups():
            if N_sub.order() > 1 and is_ab(N_sub) and H.is_normal(N_sub):
                return False
    return True

def has_larger_normal_semisimple(G, N):
    if G.order() < 60:
        return False
        
    if hasattr(G, 'normal_subgroups'):
        ns = G.normal_subgroups()
    elif hasattr(G, 'subgroups'):
        ns = [H for H in G.subgroups() if G.is_normal(H)]
    else:
        return False
        
    for H in ns:
        if is_semisimple(H):
            if strictly_contains(H, N):
                return True
    return False

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'order') and G.order() < float('inf')
    except Exception:
        h1 = False
        
    try:
        if not hasattr(N, 'generators'):
            h2 = False
        else:
            n_in_g = True
            for g in N.generators:
                if g not in G:
                    n_in_g = False
                    break
            if not n_in_g:
                h2 = False
            else:
                h2 = not has_larger_normal_semisimple(G, N)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_characteristic(G, N)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: There is no normal semisimple subgroup of G that strictly contains N",
    "¬Q: N is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2