import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from itertools import product

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is a subgroup of G
    try:
        h1_ok = all(G.contains(h) for h in H.generators)
    except Exception:
        h1_ok = False
        
    # neg_Q: H is not a characteristic subgroup of G
    try:
        neg_q_ok = False
        # A characteristic subgroup must first be a subgroup
        is_subgroup = all(G.contains(h) for h in H.generators)
        if not is_subgroup:
            is_char = False
        elif H.order() == 1 or H.order() == G.order():
            is_char = True
        else:
            gens = G.generators
            if not gens:
                is_char = True
            else:
                identity = gens[0] ** 0
                G_order = G.order()
                elements = list(G.generate())
                
                is_char = True
                # Iterate over all possible images for the generators to find automorphisms
                for images in product(elements, repeat=len(gens)):
                    mapping = {}
                    mapping[identity] = identity
                    queue = [identity]
                    head = 0
                    is_homo = True
                    
                    # BFS to build the homomorphism and check if relations are preserved
                    while head < len(queue):
                        u = queue[head]
                        head += 1
                        
                        for i, g in enumerate(gens):
                            v = u * g
                            v_img = mapping[u] * images[i]
                            if v in mapping:
                                if mapping[v] != v_img:
                                    is_homo = False
                                    break
                            else:
                                mapping[v] = v_img
                                queue.append(v)
                        if not is_homo:
                            break
                            
                    if not is_homo:
                        continue
                        
                    # Check if the homomorphism is surjective (hence an automorphism)
                    if len(set(mapping.values())) != G_order:
                        continue
                        
                    # Check if this automorphism preserves H
                    preserves_H = True
                    for x, x_img in mapping.items():
                        if H.contains(x):
                            if not H.contains(x_img):
                                preserves_H = False
                                break
                                
                    if not preserves_H:
                        is_char = False
                        break
                        
        neg_q_ok = not is_char
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let H be a subgroup of G",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1