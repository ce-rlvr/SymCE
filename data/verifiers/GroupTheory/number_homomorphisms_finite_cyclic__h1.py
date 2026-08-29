import math
from itertools import product
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def is_cyclic(G):
    if not hasattr(G, 'elements') or not hasattr(G, 'order'):
        return False
    n = G.order()
    for g in G.elements:
        if g.order() == n:
            return True
    return False

def conditions(witness):
    # Check if witness is a pair of integers (n, m)
    if isinstance(witness, (tuple, list)) and len(witness) == 2 and isinstance(witness[0], int) and isinstance(witness[1], int):
        try:
            n, m = witness
            h1 = n > 0 and m > 0
            neg_q = False  # For valid integers, the number of homomorphisms is always exactly gcd(n, m)
            return [h1, neg_q]
        except Exception:
            pass

    # Otherwise, assume witness is a pair of groups (G, H)
    try:
        G, H = witness
        n = G.order()
        m = H.order()
        h1 = is_cyclic(G) and is_cyclic(H) and n < float('inf') and m < float('inf')
    except Exception:
        h1 = False

    try:
        G, H = witness
        n = G.order()
        m = H.order()
        
        gens = G.generators
        elements_H = list(H.elements)
        id_G = G.identity
        id_H = H.identity
        
        count = 0
        # Iterate over all possible assignments of generators of G to elements of H
        for images in product(elements_H, repeat=len(gens)):
            mapping = {id_G: id_H}
            queue = [id_G]
            valid = True
            
            gen_images = dict(zip(gens, images))
            
            head = 0
            # Breadth-first search to build the homomorphism and check for well-definedness
            while head < len(queue) and valid:
                curr = queue[head]
                head += 1
                curr_img = mapping[curr]
                
                for g in gens:
                    nxt = curr * g
                    nxt_img = curr_img * gen_images[g]
                    
                    if nxt in mapping:
                        if mapping[nxt] != nxt_img:
                            valid = False
                            break
                    else:
                        mapping[nxt] = nxt_img
                        queue.append(nxt)
                        
            if valid and len(mapping) == n:
                count += 1
                
        expected = math.gcd(n, m)
        neg_q = count != expected
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Z_n and Z_m are finite cyclic groups of order n and m respectively",
    "¬Q: The number of distinct group homomorphisms from Z_n to Z_m is not exactly gcd(n, m)"
]

N_HYP = 1
NEG_Q_INDEX = 1