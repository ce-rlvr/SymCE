import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from itertools import product

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_characteristic(G, H):
    try:
        elements = list(G.generate())
        identity = next(e for e in elements if e.order() == 1)
        
        # Check if H is a subgroup of G
        if not all(h in G for h in H.generators):
            return False
            
        H_elements = list(H.generate())
        H_identity = next(e for e in H_elements if e.order() == 1)
        if H_identity not in G:
            return False
            
        gens = G.generators
        gens_orders = [g.order() for g in gens]
        # An automorphism must map a generator to an element of the same order
        valid_images = [[e for e in elements if e.order() == o] for o in gens_orders]
        
        # Test all possible mappings of generators
        for images in product(*valid_images):
            mapping = {identity: identity}
            queue = [identity]
            valid = True
            
            # BFS to build the homomorphism
            while queue:
                curr = queue.pop(0)
                for i, g in enumerate(gens):
                    nxt = curr * g
                    nxt_img = mapping[curr] * images[i]
                    if nxt in mapping:
                        if mapping[nxt] != nxt_img:
                            valid = False
                            break
                    else:
                        mapping[nxt] = nxt_img
                        queue.append(nxt)
                if not valid:
                    break
            
            # If it's a valid homomorphism and is bijective, it's an automorphism
            if valid and len(mapping) == len(elements) and len(set(mapping.values())) == len(elements):
                # Check if H is invariant under this automorphism
                for h in H.generators:
                    if mapping[h] not in H:
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_characteristic(G, H)
    except Exception:
        h1 = False
        
    try:
        h2 = is_characteristic(H, K)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_characteristic(G, K)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a characteristic subgroup of G",
    "H_2: K is a characteristic subgroup of H",
    "¬Q: K is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2