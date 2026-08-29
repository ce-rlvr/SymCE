import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_normal_subgroup(G, H):
    d = G.degree
    elements_G = set(G.elements)
    
    H_gens = [Permutation([h(i) for i in range(d)]) for h in H.generators]
    
    for h in H_gens:
        if h not in elements_G:
            return False
            
    elements_H = set(Permutation([h(i) for i in range(d)]) for h in H.elements)
    
    for g in G.generators:
        g_inv = g**-1
        for h in H_gens:
            if (g_inv * h * g) not in elements_H:
                return False
    return True

def intersection_trivial(d, H, K):
    elements_H = set(Permutation([h(i) for i in range(d)]) for h in H.elements)
    elements_K = set(Permutation([k(i) for i in range(d)]) for k in K.elements)
    intersection = elements_H.intersection(elements_K)
    return len(intersection) == 1

def direct_product(H, K):
    dH = H.degree
    dK = K.degree
    if dH == 0: dH = 1
    if dK == 0: dK = 1
    gens = []
    for g in H.generators:
        arr = [g(i) for i in range(dH)] + list(range(dH, dH + dK))
        gens.append(Permutation(arr))
    for g in K.generators:
        arr = list(range(dH)) + [dH + g(i) for i in range(dK)]
        gens.append(Permutation(arr))
    if not gens:
        return PermutationGroup([Permutation(dH + dK - 1)])
    return PermutationGroup(gens)

def quotient_group(G, H):
    d = G.degree
    elements_G = list(G.elements)
    elements_H = [Permutation([h(i) for i in range(d)]) for h in H.elements]
    
    cosets = []
    seen = set()
    for g in elements_G:
        if g not in seen:
            coset = frozenset(h * g for h in elements_H)
            cosets.append(coset)
            seen.update(coset)
            
    reps = [next(iter(c)) for c in cosets]
    elem_to_coset = {}
    for i, c in enumerate(cosets):
        for elem in c:
            elem_to_coset[elem] = i
            
    gens_quotient = []
    for g in G.generators:
        perm = []
        for rep in reps:
            target = rep * g
            perm.append(elem_to_coset[target])
        gens_quotient.append(Permutation(perm))
        
    if not gens_quotient:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens_quotient)

def conditions(witness) -> list[bool]:
    if not isinstance(witness, tuple) or len(witness) != 3:
        return [False, False, False, False]
    G, H, K = witness
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = is_normal_subgroup(G, H) and is_normal_subgroup(G, K)
    except Exception:
        h2 = False
        
    try:
        h3 = intersection_trivial(G.degree, H, K)
    except Exception:
        h3 = False
        
    try:
        HxK = direct_product(H, K)
        if G.order() != HxK.order():
            is_iso_1 = False
        else:
            is_iso_1 = G.is_isomorphic(HxK)
            
        G_mod_H = quotient_group(G, H)
        if G_mod_H.order() != K.order():
            is_iso_2 = False
        else:
            is_iso_2 = G_mod_H.is_isomorphic(K)
            
        neg_q = not (is_iso_1 and is_iso_2)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H and K are normal subgroups of G",
    "H_3: H ∩ K = {e}",
    "¬Q: G is not isomorphic to H × K or G/H is not isomorphic to K"
]

N_HYP = 3
NEG_Q_INDEX = 3