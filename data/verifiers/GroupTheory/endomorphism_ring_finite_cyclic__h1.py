import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: End(G) is the ring of group endomorphisms of G under pointwise addition and function composition",
    "¬Q: End(G) is not isomorphic to the ring Z_n of integers modulo n"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # For End(G) to be a ring under pointwise addition, G must be abelian.
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False
        
    try:
        n = witness.order()
        gens = witness.generators
        elements = list(witness.elements)
        identity = next(e for e in elements if e.is_Identity)
        
        count = 0
        # Count the number of valid endomorphisms by checking all possible mappings of the generators
        for images in itertools.product(elements, repeat=len(gens)):
            mapping = {identity: identity}
            queue = [identity]
            head = 0
            possible = True
            
            # Breadth-first search to build the full homomorphism and check for consistency
            while head < len(queue):
                g = queue[head]
                head += 1
                h = mapping[g]
                
                for gen, img in zip(gens, images):
                    next_g = g * gen
                    next_h = h * img
                    if next_g in mapping:
                        if mapping[next_g] != next_h:
                            possible = False
                            break
                    else:
                        mapping[next_g] = next_h
                        queue.append(next_g)
                if not possible:
                    break
                    
            if possible and len(mapping) == n:
                count += 1
                
        # If End(G) is isomorphic to Z_n, it must have exactly n elements.
        # For finite abelian groups, |End(G)| = n iff G is cyclic.
        # Thus, count != n is exactly when End(G) is NOT isomorphic to Z_n.
        neg_q = bool(count != n)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]