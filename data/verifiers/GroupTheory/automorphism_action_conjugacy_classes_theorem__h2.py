import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
import itertools

# Top-level setup
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

def get_automorphisms(G):
    gens = G.generators
    elements = list(G.generate())
    order = G.order()
    
    # Find the identity element safely
    id_elem = next(e for e in elements if e * e == e)
    
    if not gens:
        return [{id_elem: id_elem}]
        
    auts = []
    gen_orders = [g.order() for g in gens]
    
    for images in itertools.product(elements, repeat=len(gens)):
        # Fast filter: orders of images must match orders of generators
        if any(img.order() != go for img, go in zip(images, gen_orders)):
            continue
            
        try:
            H = PermutationGroup(images)
            if H.order() != order:
                continue
                
            # Build the homomorphism mapping via BFS on the Cayley graph
            mapping = {id_elem: id_elem}
            queue = [id_elem]
            gen_to_img = dict(zip(gens, images))
            
            is_hom = True
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    nxt = curr * g
                    nxt_img = mapping[curr] * gen_to_img[g]
                    if nxt in mapping:
                        if mapping[nxt] != nxt_img:
                            is_hom = False
                            break
                    else:
                        mapping[nxt] = nxt_img
                        queue.append(nxt)
                if not is_hom:
                    break
                    
            if is_hom and len(mapping) == order:
                auts.append(mapping)
        except Exception:
            pass
            
    return auts

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, C = witness
        else:
            G = witness
            C = None
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: C is the set of all conjugacy classes of G
    try:
        if not h1 or C is None:
            h2 = False
        else:
            actual_classes = {frozenset(cls) for cls in G.conjugacy_classes()}
            witness_classes = {frozenset(cls) for cls in C}
            h2 = (actual_classes == witness_classes)
    except Exception:
        h2 = False
        
    # neg_Q: The map Aut(G) x C -> C is a well-defined group action
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            auts = get_automorphisms(G)
            C_sets = {frozenset(cls) for cls in C}
            
            is_action = True
            
            # 1. Well-defined: phi(K) is in C for all phi in Aut(G) and K in C
            for phi in auts:
                for K in C_sets:
                    phi_K = frozenset(phi[k] for k in K)
                    if phi_K not in C_sets:
                        is_action = False
                        break
                if not is_action:
                    break
            
            # 2. Identity: The identity automorphism acts trivially on C
            if is_action:
                has_id = False
                for phi in auts:
                    acts_as_id = True
                    for K in C_sets:
                        phi_K = frozenset(phi[k] for k in K)
                        if phi_K != K:
                            acts_as_id = False
                            break
                    if acts_as_id:
                        has_id = True
                        break
                if not has_id:
                    is_action = False
            
            # 3. Compatibility: (phi1 * phi2)(K) == phi1(phi2(K))
            # Since Aut(G) is canonically a group under function composition,
            # this axiom is mathematically guaranteed to hold if the map is well-defined.
            
            neg_q = not is_action
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: C is the set of all conjugacy classes of G",
    "¬Q: The map Aut(G) x C -> C is not a well-defined group action"
]

N_HYP = 2
NEG_Q_INDEX = 2