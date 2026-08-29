import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
import itertools
import math

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

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (G, H), checks:
      H_1: G is a finite group
      H_2: G contains exactly one subgroup H of order k (where k = |H|)
      ¬Q: H is not a characteristic subgroup of G
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: G contains exactly one subgroup H of order k
    try:
        if not h1 or not isinstance(H, PermutationGroup):
            h2 = False
        else:
            g_elements_set = set(G.elements)
            if not all(g in g_elements_set for g in H.generators):
                h2 = False
            else:
                k = H.order()
                if k == G.order():
                    h2 = True
                else:
                    elements = list(G.elements)
                    identity = G.identity
                    valid_elements = [e for e in elements if k % e.order() == 0]
                    
                    if len(valid_elements) < k:
                        h2 = False
                    else:
                        def nCr(n, r):
                            if r < 0 or r > n: return 0
                            f = math.factorial
                            return f(n) // (f(r) * f(n - r))
                            
                        N = len(valid_elements)
                        if nCr(N - 1, k - 1) <= 10000:
                            valid_elements_no_id = [x for x in valid_elements if x != identity]
                            count_k = 0
                            h2 = True
                            for subset in itertools.combinations(valid_elements_no_id, k - 1):
                                subset_set = set(subset)
                                subset_set.add(identity)
                                
                                is_subgroup = True
                                for a in subset_set:
                                    for b in subset_set:
                                        if a * b not in subset_set:
                                            is_subgroup = False
                                            break
                                    if not is_subgroup:
                                        break
                                        
                                if is_subgroup:
                                    count_k += 1
                                    if count_k > 1:
                                        h2 = False
                                        break
                            if h2 and count_k == 1:
                                h2 = True
                            else:
                                h2 = False
                        else:
                            subgroups = {frozenset([identity])}
                            queue = [frozenset([identity])]
                            count_k = 0
                            h2 = True
                            
                            limit = 1000
                            while queue and len(subgroups) < limit:
                                current = queue.pop(0)
                                for e in valid_elements:
                                    if e not in current:
                                        gens_list = list(current) + [e]
                                        new_group = PermutationGroup(gens_list)
                                        order = new_group.order()
                                        if order <= k:
                                            new_elements = frozenset(new_group.elements)
                                            if new_elements not in subgroups:
                                                subgroups.add(new_elements)
                                                queue.append(new_elements)
                                                if order == k:
                                                    count_k += 1
                                                    if count_k > 1:
                                                        h2 = False
                                                        break
                                if not h2:
                                    break
                            if len(subgroups) >= limit:
                                h2 = False
                            elif h2 and count_k == 1:
                                h2 = True
                            else:
                                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: H is NOT a characteristic subgroup of G
    try:
        if not h1 or not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            g_elements_set = set(G.elements)
            if not all(g in g_elements_set for g in H.generators):
                neg_q = False
            else:
                gens = G.generators
                elements = list(G.elements)
                
                valid_images = []
                for g in gens:
                    order = g.order()
                    valid_images.append([e for e in elements if e.order() == order])
                    
                h_elements = set(H.elements)
                is_char = True
                comb_count = 0
                
                for images in itertools.product(*valid_images):
                    comb_count += 1
                    if comb_count > 5000:
                        break
                        
                    mapping = {G.identity: G.identity}
                    queue = [G.identity]
                    gen_to_img = dict(zip(gens, images))
                    
                    is_valid = True
                    while queue:
                        curr = queue.pop(0)
                        curr_img = mapping[curr]
                        
                        for g in gens:
                            nxt = curr * g
                            nxt_img = curr_img * gen_to_img[g]
                            
                            if nxt in mapping:
                                if mapping[nxt] != nxt_img:
                                    is_valid = False
                                    break
                            else:
                                mapping[nxt] = nxt_img
                                queue.append(nxt)
                        if not is_valid:
                            break
                            
                    if is_valid and len(set(mapping.values())) == G.order():
                        is_invariant = True
                        for h in h_elements:
                            if mapping[h] not in h_elements:
                                is_invariant = False
                                break
                        if not is_invariant:
                            is_char = False
                            break
                neg_q = not is_char
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G contains exactly one subgroup H of order k",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2