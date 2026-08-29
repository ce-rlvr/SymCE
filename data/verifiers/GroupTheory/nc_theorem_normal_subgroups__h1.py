import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation
from itertools import product

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

def get_quotient_group(G, C):
    C_elements = set(C.generate())
    G_elements = list(G.generate())
    
    cosets = []
    seen = set()
    for g in G_elements:
        if g not in seen:
            coset = frozenset(g * c for c in C_elements)
            cosets.append(coset)
            seen.update(coset)
            
    perms = []
    for g in G.generators:
        perm_array = [0] * len(cosets)
        for i, coset in enumerate(cosets):
            rep = next(iter(coset))
            target = g * rep
            for j, other_coset in enumerate(cosets):
                if target in other_coset:
                    perm_array[i] = j
                    break
        perms.append(Permutation(perm_array))
        
    if not perms:
        return PermutationGroup(Permutation(max(0, len(cosets)-1)))
    return PermutationGroup(*perms)

def get_automorphism_group(N):
    elements = list(N.generate())
    gens = N.generators
    id_elem = None
    for e in elements:
        if e * e == e:
            id_elem = e
            break
            
    if not gens:
        return PermutationGroup(Permutation(0))
        
    aut_perms = []
    for target_gens in product(elements, repeat=len(gens)):
        try:
            H = PermutationGroup(*target_gens)
            if H.order() != N.order():
                continue
        except Exception:
            continue
            
        element_to_word = {id_elem: []}
        frontier = [id_elem]
        while frontier:
            curr = frontier.pop(0)
            for i, g in enumerate(gens):
                nxt = curr * g
                if nxt not in element_to_word:
                    element_to_word[nxt] = element_to_word[curr] + [i]
                    frontier.append(nxt)
                    
        mapping = {}
        for elem, word in element_to_word.items():
            val = id_elem
            for idx in word:
                val = val * target_gens[idx]
            mapping[elem] = val
            
        is_homo = True
        for a in elements:
            for b in elements:
                if mapping[a * b] != mapping[a] * mapping[b]:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        if is_homo:
            perm_array = [0] * len(elements)
            for i, elem in enumerate(elements):
                mapped_elem = mapping[elem]
                perm_array[i] = elements.index(mapped_elem)
            aut_perms.append(Permutation(perm_array))
            
    if not aut_perms:
        return PermutationGroup(Permutation(max(0, len(elements)-1)))
    return PermutationGroup(*aut_perms)

def is_isomorphic_to_subgroup(Q, A):
    Q_elements = list(Q.generate())
    A_elements = list(A.generate())
    
    Q_gens = Q.generators
    if not Q_gens:
        return True
        
    id_Q = None
    for e in Q_elements:
        if e * e == e:
            id_Q = e
            break
            
    id_A = None
    for e in A_elements:
        if e * e == e:
            id_A = e
            break
            
    for target_gens in product(A_elements, repeat=len(Q_gens)):
        try:
            H = PermutationGroup(*target_gens)
            if H.order() != Q.order():
                continue
        except Exception:
            continue
            
        element_to_word = {id_Q: []}
        frontier = [id_Q]
        while frontier:
            curr = frontier.pop(0)
            for i, g in enumerate(Q_gens):
                nxt = curr * g
                if nxt not in element_to_word:
                    element_to_word[nxt] = element_to_word[curr] + [i]
                    frontier.append(nxt)
                    
        mapping = {}
        for elem, word in element_to_word.items():
            val = id_A
            for idx in word:
                val = val * target_gens[idx]
            mapping[elem] = val
            
        is_homo = True
        for a in Q_elements:
            for b in Q_elements:
                if mapping[a * b] != mapping[a] * mapping[b]:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        if is_homo:
            return True
            
    return False

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    # H1: N is a normal subgroup of G
    try:
        G_elements = set(G.generate())
        is_subgroup = True
        for gen in N.generators:
            if gen not in G_elements:
                is_subgroup = False
                break
                
        is_normal = is_subgroup
        if is_subgroup:
            N_elements = set(N.generate())
            for g in G.generators:
                for n in N.generators:
                    if g * n * ~g not in N_elements:
                        is_normal = False
                        break
                if not is_normal:
                    break
        h1_ok = is_normal
    except Exception:
        h1_ok = False

    # Conclusion: G/C_G(N) is isomorphic to a subgroup of Aut(N)
    try:
        N_gens = N.generators
        C_elements = []
        for g in G.generate():
            if all(g * n == n * g for n in N_gens):
                C_elements.append(g)
                
        if not C_elements:
            id_G = None
            for e in G.generate():
                if e * e == e:
                    id_G = e
                    break
            C_G_N = PermutationGroup(id_G)
        else:
            C_G_N = PermutationGroup(*C_elements)
            
        C_elements_set = set(C_G_N.generate())
        c_is_normal = True
        for g in G.generators:
            for c in C_G_N.generators:
                if g * c * ~g not in C_elements_set:
                    c_is_normal = False
                    break
            if not c_is_normal:
                break
                
        if not c_is_normal:
            q_ok = False
        else:
            Q = get_quotient_group(G, C_G_N)
            A = get_automorphism_group(N)
            q_ok = is_isomorphic_to_subgroup(Q, A)
    except Exception:
        q_ok = False

    neg_q = not q_ok
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: G/C_G(N) is not isomorphic to a subgroup of Aut(N)"
]
N_HYP = 1
NEG_Q_INDEX = 1