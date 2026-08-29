import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import Permutation, PermutationGroup
from itertools import product

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_automorphisms(G):
    """Computes the automorphism group of a permutation group G."""
    elements = list(G.generate())
    n = len(elements)
    if n == 1:
        return PermutationGroup([Permutation([0])])
        
    # Find identity element
    identity = None
    for e in elements:
        if e * e == e:
            identity = e
            break
            
    elem_idx = {e: i for i, e in enumerate(elements)}
    mult = [[elem_idx[e1 * e2] for e2 in elements] for e1 in elements]
    
    gens_idx = [elem_idx[g] for g in G.generators]
    
    # Precompute a word (in terms of generators) for each element using BFS
    words = {elem_idx[identity]: []}
    queue = [elem_idx[identity]]
    while queue:
        curr = queue.pop(0)
        for i, g_i in enumerate(gens_idx):
            nxt = mult[curr][g_i]
            if nxt not in words:
                words[nxt] = words[curr] + [i]
                queue.append(nxt)
                
    auts = []
    # Test all possible mappings of the generators
    for target_idx in product(range(n), repeat=len(gens_idx)):
        mapping = {}
        # Evaluate the word for each element under the new generator mapping
        for i in range(n):
            curr = elem_idx[identity]
            for gen_idx in words[i]:
                curr = mult[curr][target_idx[gen_idx]]
            mapping[i] = curr
            
        # An automorphism must be a bijection
        if len(set(mapping.values())) != n:
            continue
            
        # Check if the mapping is a valid homomorphism
        valid = True
        for i in range(n):
            for j in range(n):
                if mapping[mult[i][j]] != mult[mapping[i]][mapping[j]]:
                    valid = False
                    break
            if not valid:
                break
                
        if valid:
            auts.append([mapping[i] for i in range(n)])
            
    aut_perms = [Permutation(p) for p in auts]
    return PermutationGroup(aut_perms)

def get_center_order(G):
    """Computes the order of the center of G."""
    elements = list(G.generate())
    center_size = 0
    for e in elements:
        if all(e * x == x * e for x in elements):
            center_size += 1
    return center_size

def is_complete(G):
    """
    A group is complete if its center is trivial and every automorphism is inner.
    This is equivalent to |Z(G)| == 1 and |Aut(G)| == |G|.
    """
    if get_center_order(G) != 1:
        return False
    auts = get_automorphisms(G)
    if auts is None:
        return False
    return auts.order() == G.order()

def conditions(witness):
    try:
        # H_1: G is a simple group
        # A group is simple if it is non-trivial and its only normal subgroups are itself and the trivial group.
        if witness.order() == 1:
            h1 = False
        else:
            h1 = len(witness.normal_subgroups()) == 2
    except Exception:
        h1 = False

    try:
        # Q: Aut(G) is a complete group
        # neg_Q: Aut(G) is NOT a complete group
        aut_G = get_automorphisms(witness)
        if aut_G is None:
            neg_q = False
        else:
            q = is_complete(aut_G)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a simple group",
    "¬Q: Aut(G) is not a complete group"
]

N_HYP = 1
NEG_Q_INDEX = 1