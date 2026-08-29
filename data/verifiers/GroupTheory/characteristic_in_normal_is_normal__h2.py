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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_characteristic(N, K):
    if not all(g in N for g in K.generators):
        return False
    
    elements = list(N.generate())
    gens = N.generators
    n_order = len(elements)
    
    # Precompute a word (sequence of generator indices) for each element in N
    word_for = {}
    word_for[N.identity] = []
    queue = [N.identity]
    while queue:
        curr = queue.pop(0)
        for i, g in enumerate(gens):
            nxt = curr * g
            if nxt not in word_for:
                word_for[nxt] = word_for[curr] + [i]
                queue.append(nxt)
                
    K_elems = set(K.generate())
    
    # Check all possible assignments of generators to elements in N
    for images in itertools.product(elements, repeat=len(gens)):
        # An automorphism must preserve the order of generators
        if any(images[i].order() != gens[i].order() for i in range(len(gens))):
            continue
            
        # The images must generate the whole group N
        if PermutationGroup(*images).order() != n_order:
            continue
            
        # Build the mapping defined by this generator assignment
        mapping = {}
        for elem in elements:
            val = N.identity
            for idx in word_for[elem]:
                val = val * images[idx]
            mapping[elem] = val
            
        # Verify it is a valid homomorphism
        is_homo = True
        for x in elements:
            for i, y in enumerate(gens):
                if mapping[x * y] != mapping[x] * images[i]:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        if is_homo:
            # It is an automorphism. Check if K is invariant.
            for k_gen in K.generators:
                if mapping[k_gen] not in K_elems:
                    return False
                    
    return True

def is_normal_safe(K, G):
    if not all(g in G for g in K.generators):
        return False
    K_elems = set(K.generate())
    for g in G.generators:
        g_inv = ~g
        for k in K.generators:
            if g * k * g_inv not in K_elems:
                return False
    return True

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, N, K = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group, N is a subgroup of G
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(K, PermutationGroup):
            h1_ok = all(g in G for g in N.generators)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False
        
    # H2: K is a characteristic subgroup of N
    try:
        h2_ok = is_characteristic(N, K)
    except Exception:
        h2_ok = False
        
    # neg_Q: K is NOT a normal subgroup of G
    try:
        neg_q_ok = not is_normal_safe(K, G)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "H_2: K is a characteristic subgroup of N",
    "¬Q: K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2