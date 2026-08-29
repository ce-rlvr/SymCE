import itertools
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_automorphism_group_Z2(G):
    """
    Returns True if the automorphism group of G is isomorphic to Z2.
    Since the only group of order 2 is Z2, this is equivalent to checking
    if the number of automorphisms of G is exactly 2.
    """
    try:
        if not hasattr(G, 'generators') or not hasattr(G, 'order'):
            return False
        gens = G.generators
        elements = list(G.generate())
        
        if G.order() == 1:
            return False
            
        # Find the identity element of the group
        identity = next(e for e in elements if e * e == e)
            
        auts_count = 0
        # An automorphism is uniquely determined by its action on the generators.
        # We iterate over all possible mappings of the generators.
        for target in itertools.product(elements, repeat=len(gens)):
            # The image of the generators must generate a subgroup of the same order (i.e., the whole group)
            H = PermutationGroup(*target)
            if H.order() != G.order():
                continue
                
            mapping = {identity: identity}
            valid = True
            queue = [identity]
            
            # Breadth-first search to build the full homomorphism and check for contradictions
            for _ in range(G.order()):
                new_queue = []
                for curr in queue:
                    for i, g in enumerate(gens):
                        nxt = curr * g
                        nxt_val = mapping[curr] * target[i]
                        if nxt in mapping:
                            if mapping[nxt] != nxt_val:
                                valid = False
                                break
                        else:
                            mapping[nxt] = nxt_val
                            new_queue.append(nxt)
                    if not valid:
                        break
                if not valid:
                    break
                queue = new_queue
                if not queue:
                    break
                    
            # If it's a valid homomorphism and surjective (hence bijective since G is finite)
            if valid and len(mapping) == G.order():
                auts_count += 1
                if auts_count > 2:
                    return False
                    
        return auts_count == 2
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            # The conclusion is that Aut(G) is isomorphic to Z2.
            # We want neg_q to be True when the conclusion FAILS.
            q = is_automorphism_group_Z2(witness)
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Aut(G) is not isomorphic to the cyclic group of order 2"
]
N_HYP = 0
NEG_Q_INDEX = 0