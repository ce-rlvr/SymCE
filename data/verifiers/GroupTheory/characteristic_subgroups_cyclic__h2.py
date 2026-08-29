import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a cyclic group
    try:
        if hasattr(G, 'is_cyclic'):
            h1 = bool(G.is_cyclic)
        else:
            order = G.order()
            h1 = any(g.order() == order for g in G.generate())
    except Exception:
        h1 = False
        
    # neg_Q: H is NOT a characteristic subgroup of G
    try:
        # 1. Extract elements of H
        try:
            if hasattr(H, 'generate'):
                H_elements = list(H.generate())
            else:
                H_elements = list(H)
        except Exception:
            H_elements = []
            
        # 2. Check if H is a subgroup of G
        try:
            G_elements = list(G.generate())
            if not G_elements:
                is_sub = False
            else:
                identity = G_elements[0]**0
                is_sub = True
                if not all(h in G_elements for h in H_elements):
                    is_sub = False
                elif identity not in H_elements:
                    is_sub = False
                else:
                    H_set = set(H_elements)
                    for x in H_elements:
                        if ~x not in H_set:
                            is_sub = False
                            break
                        for y in H_elements:
                            if x*y not in H_set:
                                is_sub = False
                                break
        except Exception:
            is_sub = False
            
        if not is_sub:
            # If it's not a subgroup, it's not a characteristic subgroup
            neg_q = True
        else:
            # 3. Check if H is invariant under all automorphisms of G
            try:
                gens = G.generators
                
                # Precompute a word (sequence of generators) for each element in G
                words = {identity: []}
                queue = [identity]
                while queue:
                    curr = queue.pop(0)
                    for i, gen in enumerate(gens):
                        nxt = curr * gen
                        if nxt not in words:
                            words[nxt] = words[curr] + [i]
                            queue.append(nxt)
                            
                # Find all possible valid images for the generators (must preserve order)
                valid_images = []
                for gen in gens:
                    order = gen.order()
                    valid_images.append([e for e in G_elements if e.order() == order])
                    
                is_char = True
                H_set = set(H_elements)
                
                # Iterate over all candidate generator assignments
                for img_tuple in itertools.product(*valid_images):
                    mapping = {}
                    for g in G_elements:
                        val = identity
                        for idx in words[g]:
                            val = val * img_tuple[idx]
                        mapping[g] = val
                        
                    # Check if mapping is a bijection
                    if len(set(mapping.values())) != len(G_elements):
                        continue
                        
                    # Check if mapping is a homomorphism
                    is_hom = True
                    for x in G_elements:
                        mx = mapping[x]
                        for y in G_elements:
                            if mx * mapping[y] != mapping[x * y]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                            
                    if is_hom:
                        # It is a valid automorphism; check if H is invariant
                        H_mapped = {mapping[h] for h in H_elements}
                        if H_mapped != H_set:
                            is_char = False
                            break
                            
                neg_q = not is_char
            except Exception:
                neg_q = False
                
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1