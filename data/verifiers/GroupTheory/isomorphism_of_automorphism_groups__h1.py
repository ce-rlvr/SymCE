import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_automorphism_group(G):
    """Computes the automorphism group of a permutation group G."""
    elements = list(G.generate())
    n = len(elements)
    if n == 1:
        return PermutationGroup([Permutation([0])])
        
    identity = elements[0] * elements[0]**-1
    
    gens = G.generators
    gens_with_inv = []
    for g in gens:
        gens_with_inv.append(g)
        gens_with_inv.append(g**-1)
        
    gen_orders = [g.order() for g in gens]
    automorphisms = []
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    for target_gens in itertools.product(elements, repeat=len(gens)):
        if any(tg.order() != o for tg, o in zip(target_gens, gen_orders)):
            continue
            
        gen_map = {}
        for g, tg in zip(gens, target_gens):
            gen_map[g] = tg
        for g in gens:
            gen_map[g**-1] = gen_map[g]**-1
            
        mapping = {identity: identity}
        valid = True
        
        queue = [identity]
        visited = {identity}
        
        # BFS to extend the homomorphism and check relations
        while queue and valid:
            curr = queue.pop(0)
            for g in gens_with_inv:
                nxt = curr * g
                t_nxt = mapping[curr] * gen_map[g]
                if nxt not in visited:
                    mapping[nxt] = t_nxt
                    visited.add(nxt)
                    queue.append(nxt)
                else:
                    if mapping[nxt] != t_nxt:
                        valid = False
                        break
                        
        if valid and len(set(mapping.values())) == n:
            perm_array = [0] * n
            for e in elements:
                perm_array[elem_to_idx[e]] = elem_to_idx[mapping[e]]
            automorphisms.append(Permutation(perm_array))
            
    if not automorphisms:
        automorphisms.append(Permutation(list(range(n))))
        
    return PermutationGroup(automorphisms)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(G.is_isomorphic(H))
    except Exception:
        h1 = False
        
    try:
        aut_G = get_automorphism_group(G)
        aut_H = get_automorphism_group(H)
        q = bool(aut_G.is_isomorphic(aut_H))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is isomorphic to H",
    "¬Q: Aut(G) is not isomorphic to Aut(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1