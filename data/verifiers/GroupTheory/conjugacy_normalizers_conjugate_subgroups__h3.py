import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def pad_perm(p, size):
    if p.size == size:
        return p
    elif p.size < size:
        return Permutation(p.array_form + list(range(p.size, size)))
    else:
        if all(p.array_form[i] == i for i in range(size, p.size)):
            return Permutation(p.array_form[:size])
        return p

def get_padded_elems(group, size):
    return {pad_perm(g, size) for g in group.generate()}

def get_padded_generators(group, size):
    return [pad_perm(g, size) for g in group.generators]

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H and K are subgroups of G
    try:
        def is_subgroup(sub, super_group):
            if not isinstance(sub, PermutationGroup):
                return False
            super_elems = set(super_group.generate())
            sub_gens = get_padded_generators(sub, super_group.degree)
            for g in sub_gens:
                if g not in super_elems:
                    return False
            return True
            
        h2 = is_subgroup(H, G) and is_subgroup(K, G)
    except Exception:
        h2 = False
        
    # ¬Q: N_G(H) is NOT conjugate to N_G(K) in G
    try:
        def get_normalizer_elems(G, H):
            H_elems = get_padded_elems(H, G.degree)
            H_gens = get_padded_generators(H, G.degree)
            norm_elems = set()
            for g in G.generate():
                is_norm = True
                for h in H_gens:
                    if (g * h * ~g) not in H_elems:
                        is_norm = False
                        break
                if is_norm:
                    norm_elems.add(g)
            return norm_elems
            
        N_H_elems = get_normalizer_elems(G, H)
        N_K_elems = get_normalizer_elems(G, K)
        
        def are_conjugate(G, A_elems, B_elems):
            if len(A_elems) != len(B_elems):
                return False
            for g in G.generate():
                is_conj = True
                for a in A_elems:
                    if (g * a * ~g) not in B_elems:
                        is_conj = False
                        break
                if is_conj:
                    return True
            return False
            
        neg_q = not are_conjugate(G, N_H_elems, N_K_elems)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H and K are subgroups of G",
    "¬Q: N_G(H) is not conjugate to N_G(K) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2