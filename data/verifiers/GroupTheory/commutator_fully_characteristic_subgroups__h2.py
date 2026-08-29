import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group and H, K are subgroups of G",
    "¬Q: The mutual commutator subgroup of H and K is not a fully characteristic subgroup of G"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False]
        G, H, K = witness
    except Exception:
        return [False, False]
        
    h1_ok = False
    H_norm = None
    K_norm = None
    G_elements = None
    id_G = None
    
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup):
            G_elements = set(G.generate())
            
            def stripped(perm):
                arr = list(perm.array_form)
                while arr and arr[-1] == len(arr) - 1:
                    arr.pop()
                return arr
                
            G_stripped = {tuple(stripped(g)): g for g in G_elements}
            
            h_sub = True
            H_gens_G = []
            for g in H.generators:
                s = tuple(stripped(g))
                if s in G_stripped:
                    H_gens_G.append(G_stripped[s])
                else:
                    h_sub = False
                    break
                    
            k_sub = True
            K_gens_G = []
            for g in K.generators:
                s = tuple(stripped(g))
                if s in G_stripped:
                    K_gens_G.append(G_stripped[s])
                else:
                    k_sub = False
                    break
                    
            if h_sub and k_sub:
                h1_ok = True
                id_G = list(G_elements)[0]**0
                H_norm = PermutationGroup(H_gens_G) if H_gens_G else PermutationGroup([id_G])
                K_norm = PermutationGroup(K_gens_G) if K_gens_G else PermutationGroup([id_G])
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        if h1_ok:
            # Compute the mutual commutator subgroup of H and K
            comm_gens = []
            for h in H_norm.generate():
                for k in K_norm.generate():
                    c = h * k * (h**-1) * (k**-1)
                    comm_gens.append(c)
            HK_comm = PermutationGroup(comm_gens) if comm_gens else PermutationGroup([id_G])
            
            # Get all endomorphisms of G
            elements = list(G_elements)
            n = len(elements)
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            
            gens = G.generators
            inv_gens = [g**-1 for g in gens]
            all_gens = gens + inv_gens
            
            # Precompute transitions for fast homomorphism checking
            transition = [[0]*len(all_gens) for _ in range(n)]
            for i in range(n):
                for j, g in enumerate(all_gens):
                    transition[i][j] = elem_to_idx[elements[i] * g]
                    
            # Build a spanning tree of the Cayley graph to define mappings
            word_for_elem = {elem_to_idx[id_G]: []}
            queue = [elem_to_idx[id_G]]
            
            while queue:
                curr_idx = queue.pop(0)
                curr_word = word_for_elem[curr_idx]
                
                for j in range(len(all_gens)):
                    nxt_idx = transition[curr_idx][j]
                    if nxt_idx not in word_for_elem:
                        word_for_elem[nxt_idx] = curr_word + [j]
                        queue.append(nxt_idx)
                        
            endomorphisms = []
            for target_gens in itertools.product(elements, repeat=len(gens)):
                target_all_gens = list(target_gens) + [g**-1 for g in target_gens]
                
                mapping = [None] * n
                for idx, word in word_for_elem.items():
                    val = id_G
                    for w in word:
                        val = val * target_all_gens[w]
                    mapping[idx] = val
                    
                # Verify if the mapping preserves the group structure
                is_homo = True
                for i in range(n):
                    if not is_homo:
                        break
                    for j, g in enumerate(all_gens):
                        g_idx = elem_to_idx[g]
                        xy_idx = transition[i][j]
                        if mapping[xy_idx] != mapping[i] * mapping[g_idx]:
                            is_homo = False
                            break
                if is_homo:
                    endomorphisms.append(mapping)
            
            # Check if commutator subgroup is fully characteristic
            HK_elements = set(HK_comm.generate())
            HK_indices = {elem_to_idx[e] for e in HK_elements}
            
            is_fully_char = True
            for mapping in endomorphisms:
                if not is_fully_char:
                    break
                for n_elem in HK_elements:
                    n_idx = elem_to_idx[n_elem]
                    mapped_val = mapping[n_idx]
                    if elem_to_idx[mapped_val] not in HK_indices:
                        is_fully_char = False
                        break
                        
            neg_q = not is_fully_char
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]