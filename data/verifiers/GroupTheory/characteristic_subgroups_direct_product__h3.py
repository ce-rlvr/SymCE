import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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
trivial = CyclicGroup(1)
V4 = DihedralGroup(2)

def is_subgroup_robust(A, G):
    if not isinstance(A, PermutationGroup):
        return False
    for g in A.generators:
        p = list(g.array_form)
        # Remove trailing fixed points
        while len(p) > G.degree and p[-1] == len(p) - 1:
            p.pop()
        if len(p) > G.degree:
            return False
        if len(p) < G.degree:
            p += list(range(len(p), G.degree))
        if Permutation(p) not in G:
            return False
    return True

def is_characteristic(G, A):
    if not is_subgroup_robust(A, G):
        return False
    
    if G.order() == 1:
        return A.order() == 1
        
    A_gens = []
    for g in A.generators:
        p = list(g.array_form)
        while len(p) > G.degree and p[-1] == len(p) - 1:
            p.pop()
        if len(p) < G.degree:
            p += list(range(len(p), G.degree))
        A_gens.append(Permutation(p))
    A_in_G = PermutationGroup(*A_gens) if A_gens else PermutationGroup(Permutation(G.degree - 1))

    gens = G.generators
    if not gens:
        gens = [Permutation(G.degree - 1)]
        
    G_order = G.order()
    G_elements = list(G.elements)
    G_identity = G.identity
    
    gen_orders = [g.order() for g in gens]
    elements_by_order = {}
    for g in G_elements:
        elements_by_order.setdefault(g.order(), []).append(g)
        
    valid_images_per_gen = [elements_by_order.get(o, []) for o in gen_orders]
    
    for imgs in itertools.product(*valid_images_per_gen):
        try:
            # Fast BFS to check if the mapping extends to a valid automorphism
            mapping = {G_identity: G_identity}
            queue = [G_identity]
            is_valid = True
            
            while queue and is_valid:
                curr = queue.pop(0)
                curr_img = mapping[curr]
                for g, img in zip(gens, imgs):
                    nxt = curr * g
                    nxt_img = curr_img * img
                    if nxt in mapping:
                        if mapping[nxt] != nxt_img:
                            is_valid = False
                            break
                    else:
                        mapping[nxt] = nxt_img
                        queue.append(nxt)
            
            # Must be a valid homomorphism and bijective (image size == G_order)
            if not is_valid or len(set(mapping.values())) != G_order:
                continue
                
            # Check if the automorphism preserves A
            preserves_A = True
            for a in A_in_G.generators:
                if a not in mapping or mapping[a] not in A_in_G:
                    preserves_A = False
                    break
            if not preserves_A:
                return False
                
        except Exception:
            continue
            
    return True

def get_direct_product_subgroup(G, H, A, B):
    gens = []
    for g in A.generators:
        p = list(g.array_form)
        while len(p) > G.degree and p[-1] == len(p) - 1:
            p.pop()
        if len(p) < G.degree:
            p += list(range(len(p), G.degree))
        p += list(range(G.degree, G.degree + H.degree))
        gens.append(Permutation(p))
    for h in B.generators:
        p = list(range(G.degree))
        h_arr = list(h.array_form)
        while len(h_arr) > H.degree and h_arr[-1] == len(h_arr) - 1:
            h_arr.pop()
        if len(h_arr) < H.degree:
            h_arr += list(range(len(h_arr), H.degree))
        p += [x + G.degree for x in h_arr]
        gens.append(Permutation(p))
    if not gens:
        return PermutationGroup(Permutation(G.degree + H.degree - 1))
    return PermutationGroup(*gens)

def conditions(witness):
    try:
        G, H, A, B = witness
    except Exception:
        return [False, False, False]
        
    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: A is a characteristic subgroup of G
    try:
        h2 = is_characteristic(G, A)
    except Exception:
        h2 = False
        
    # neg_Q: A x B is NOT a characteristic subgroup of G x H
    try:
        if not isinstance(B, PermutationGroup):
            neg_q = False
        else:
            GxH = get_direct_product_subgroup(G, H, G, H)
            AxB = get_direct_product_subgroup(G, H, A, B)
            neg_q = not is_characteristic(GxH, AxB)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A is a characteristic subgroup of G",
    "¬Q: A x B is not a characteristic subgroup of G x H"
]

N_HYP = 2
NEG_Q_INDEX = 2