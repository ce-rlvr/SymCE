import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def direct_product(G, H):
    """Constructs the direct product of two permutation groups."""
    deg_G = G.degree
    deg_H = H.degree
    
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < deg_G:
            arr.extend(range(len(arr), deg_G))
        arr.extend(range(deg_G, deg_G + deg_H))
        gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(h.array_form)
        if len(arr) < deg_H:
            arr.extend(range(len(arr), deg_H))
        arr_shifted = list(range(deg_G)) + [x + deg_G for x in arr]
        gens.append(Permutation(arr_shifted))
        
    if not gens:
        return PermutationGroup([Permutation([])])
    return PermutationGroup(gens)

def is_complete(G):
    """
    Checks if a permutation group is complete.
    A group is complete if its center is trivial and every automorphism is inner.
    """
    try:
        # A complete group must have a trivial center
        if G.center().order() != 1:
            return False
            
        try:
            order = G.order()
        except TypeError:
            order = G.order
            
        # Limit size to prevent timeouts on extremely large groups
        if order > 500:
            return False
            
        elements = list(G.generate())
        n = len(elements)
        
        gens = G.generators
        gen_orders = [g.order() for g in gens]
        
        # An automorphism must map generators to elements of the same order
        valid_images = [[e for e in elements if e.order() == o] for o in gen_orders]
        
        # Prevent timeout on groups with too many combinations
        num_combinations = 1
        for v in valid_images:
            num_combinations *= len(v)
            
        if num_combinations > 100000:
            return False
            
        # Precompute a BFS tree to evaluate words in generators
        path = {G.identity: None}
        queue = [G.identity]
        for e in queue:
            for i, g in enumerate(gens):
                nxt = e * g
                if nxt not in path:
                    path[nxt] = (e, i)
                    queue.append(nxt)
                    
        aut_count = 0
        for img_tuple in itertools.product(*valid_images):
            mapping = {G.identity: G.identity}
            for e in queue[1:]:
                prev_e, i = path[e]
                mapping[e] = mapping[prev_e] * img_tuple[i]
                
            # Check if the mapping preserves the group operation
            is_hom = True
            for e in elements:
                for i, g in enumerate(gens):
                    if mapping[e * g] != mapping[e] * img_tuple[i]:
                        is_hom = False
                        break
                if not is_hom:
                    break
                    
            if is_hom:
                # Check if the homomorphism is bijective
                if len(set(mapping.values())) == n:
                    aut_count += 1
                    
        # Since Z(G) is trivial, Inn(G) has size |G|.
        # G is complete iff |Aut(G)| == |Inn(G)| == |G|.
        return aut_count == n
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G is a complete group
    try:
        h2 = h1 and is_complete(G)
    except Exception:
        h2 = False
        
    # ¬Q: G \times H is NOT a complete group
    try:
        if not h1:
            neg_q = False
        else:
            GxH = direct_product(G, H)
            neg_q = not is_complete(GxH)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is a complete group",
    "¬Q: G \\times H is not a complete group"
]

N_HYP = 2
NEG_Q_INDEX = 2