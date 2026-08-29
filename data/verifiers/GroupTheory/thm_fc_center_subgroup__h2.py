import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup
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

def get_S_list(G, S):
    if isinstance(S, PermutationGroup):
        return list(S.generate())
    elif isinstance(S, (list, set, tuple)):
        return list(S)
    else:
        return None

def is_characteristic(G, S_list):
    elements = list(G.generate())
    gens = G.generators
    if not elements:
        return False
    
    # Safely get the identity element of the group
    id_elem = elements[0] * ~elements[0]
    
    S_set = set(S_list)
    
    # Check if S is a subgroup
    if id_elem not in S_set: 
        return False
    for a in S_list:
        if ~a not in S_set: 
            return False
        for b in S_list:
            if a * b not in S_set: 
                return False
            
    # Check if S is a normal subgroup (characteristic implies normal)
    for g in elements:
        g_inv = ~g
        for s in S_list:
            if g * s * g_inv not in S_set:
                return False
                
    # Precompute a word for each element in terms of the generators
    word_of = {id_elem: []}
    queue = [id_elem]
    while queue:
        curr = queue.pop(0)
        for g in gens:
            nxt = curr * g
            if nxt not in word_of:
                word_of[nxt] = word_of[curr] + [g]
                queue.append(nxt)
                
    # Check all possible assignments of generators to find automorphisms
    for img in itertools.product(elements, repeat=len(gens)):
        gen_map = dict(zip(gens, img))
        
        # Evaluate the mapping for all elements
        mapping = {}
        for elem, word in word_of.items():
            val = id_elem
            for w in word:
                val = val * gen_map[w]
            mapping[elem] = val
            
        # An endomorphism of a finite group is an automorphism iff it is bijective
        if len(set(mapping.values())) != len(elements):
            continue
            
        # Check if the mapping is a homomorphism
        is_homo = True
        for a in elements:
            for g in gens:
                if mapping[a * g] != mapping[a] * mapping[g]:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        if is_homo:
            # It is an automorphism! Check if S is invariant under it
            for s in S_list:
                if mapping[s] not in S_set:
                    return False
                    
    return True

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, S = witness
        
        # Limit group order to prevent DOS on brute-force automorphism search
        if not isinstance(G, PermutationGroup) or G.order() > 120:
            h1 = False
        else:
            S_list = get_S_list(G, S)
            if S_list is None:
                h1 = False
            else:
                G_elements = set(G.generate())
                h1 = all(s in G_elements for s in S_list)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            S_list = get_S_list(G, S)
            # neg_q is True if S is NOT a characteristic subgroup
            neg_q = not is_characteristic(G, S_list)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: S is not a characteristic subgroup of G"
]
N_HYP = 1
NEG_Q_INDEX = 1