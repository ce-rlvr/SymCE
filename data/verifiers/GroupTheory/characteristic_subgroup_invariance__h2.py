import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))

def is_characteristic(G, H):
    """
    Checks if H is a characteristic subgroup of G by finding all automorphisms of G
    and verifying if H is invariant under all of them.
    """
    elements = list(G.generate())
    gens = G.generators
    
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    n = len(elements)
    
    # Precompute multiplication table for fast homomorphism evaluation
    mul_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mul_table[i][j] = elem_to_idx[elements[i] * elements[j]]
            
    h_elements = list(H.generate())
    h_indices = {elem_to_idx[e] for e in h_elements if e in elem_to_idx}
    if len(h_indices) != len(h_elements):
        return False
        
    gen_indices = [elem_to_idx[g] for g in gens]
    
    # Iterate over all possible mappings of generators to elements of G
    for target_gens in itertools.product(range(n), repeat=len(gens)):
        eval_map = {elem_to_idx[G.identity]: elem_to_idx[G.identity]}
        queue = [elem_to_idx[G.identity]]
        head = 0
        valid = True
        
        # BFS to evaluate the homomorphism
        while head < len(queue):
            curr = queue[head]
            head += 1
            for i, g_idx in enumerate(gen_indices):
                nxt = mul_table[curr][g_idx]
                nxt_val = mul_table[eval_map[curr]][target_gens[i]]
                if nxt in eval_map:
                    if eval_map[nxt] != nxt_val:
                        valid = False
                        break
                else:
                    eval_map[nxt] = nxt_val
                    queue.append(nxt)
            if not valid:
                break
                
        # If it's a valid homomorphism and bijective, it's an automorphism
        if valid and len(eval_map) == n and len(set(eval_map.values())) == n:
            mapped_h = {eval_map[h] for h in h_indices}
            if mapped_h != h_indices:
                return False # Found an automorphism that does not preserve H
                
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
        else:
            G, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: Aut(G) is the automorphism group of G
    # This is a definitional hypothesis, inherently true if G is a group.
    try:
        h2 = h1
    except Exception:
        h2 = False
        
    # H_3: Aut(G) acts on the set of all subgroups of G
    # This requires H to be a valid subgroup of G.
    try:
        h3 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h3 = False
        
    # neg_Q: The subgroup H is NOT a fixed point under the action of Aut(G)
    # i.e., H is NOT a characteristic subgroup of G.
    try:
        if not (h1 and h3):
            neg_q = False
        else:
            neg_q = not is_characteristic(G, H)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Aut(G) is the automorphism group of G",
    "H_3: Aut(G) acts on the set of all subgroups of G",
    "¬Q: The subgroup H is not a fixed point under the action of Aut(G) (i.e. H is not characteristic)"
]

N_HYP = 3
NEG_Q_INDEX = 3