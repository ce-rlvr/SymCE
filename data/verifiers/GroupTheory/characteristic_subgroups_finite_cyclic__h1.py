import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import product

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
Klein4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is a subgroup of G
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            h1_ok = bool(H.is_subgroup(G))
        else:
            h1_ok = False
    except Exception:
        h1_ok = False
        
    # neg_Q: H is not a characteristic subgroup of G
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            is_char = True
            elements = list(G.generate())
            n = len(elements)
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            
            # Precompute multiplication table
            mult_table = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
                    
            # Find identity index
            id_idx = None
            for i, e in enumerate(elements):
                if getattr(e, 'is_Identity', False):
                    id_idx = i
                    break
            if id_idx is None:
                for i, e in enumerate(elements):
                    if e * e == e:
                        id_idx = i
                        break
                        
            # Map H elements to indices
            H_set = set()
            for h in H.generate():
                if h in elem_to_idx:
                    H_set.add(elem_to_idx[h])
                else:
                    matched = False
                    for e in elements:
                        if e == h:
                            H_set.add(elem_to_idx[e])
                            matched = True
                            break
                    if not matched:
                        arr_h = h.array_form
                        if len(arr_h) < getattr(G, 'degree', len(arr_h)):
                            arr_h = arr_h + list(range(len(arr_h), G.degree))
                        elif len(arr_h) > getattr(G, 'degree', 0):
                            if arr_h[G.degree:] == list(range(G.degree, len(arr_h))):
                                arr_h = arr_h[:G.degree]
                        try:
                            h_adj = Permutation(arr_h)
                            if h_adj in elem_to_idx:
                                H_set.add(elem_to_idx[h_adj])
                                matched = True
                        except Exception:
                            pass
                        
                    if not matched:
                        raise ValueError("H is not a subset of G")
            
            gens = G.generators
            gen_indices = [elem_to_idx[g] for g in gens]
            
            # Find candidates for mapping generators
            candidates = []
            for g_idx in gen_indices:
                order_g = elements[g_idx].order()
                cands = [i for i, e in enumerate(elements) if e.order() == order_g]
                candidates.append(cands)
                
            # Check all possible homomorphisms
            for img_indices in product(*candidates):
                mapping = {id_idx: id_idx}
                valid = True
                for g_idx, img_idx in zip(gen_indices, img_indices):
                    if g_idx in mapping:
                        if mapping[g_idx] != img_idx:
                            valid = False
                            break
                    else:
                        mapping[g_idx] = img_idx
                if not valid:
                    continue
                    
                # Extend mapping to the whole group using BFS
                queue = [id_idx] + list(gen_indices)
                head = 0
                while head < len(queue):
                    u = queue[head]
                    head += 1
                    for v in gen_indices:
                        uv = mult_table[u][v]
                        mapped_uv = mult_table[mapping[u]][mapping[v]]
                        if uv in mapping:
                            if mapping[uv] != mapped_uv:
                                valid = False
                                break
                        else:
                            mapping[uv] = mapped_uv
                            queue.append(uv)
                    if not valid:
                        break
                        
                if not valid or len(mapping) != n:
                    continue
                    
                # Check if it's an isomorphism (bijection)
                if len(set(mapping.values())) != n:
                    continue
                    
                # Check if H is invariant under this automorphism
                invariant = True
                for h_idx in H_set:
                    if mapping[h_idx] not in H_set:
                        invariant = False
                        break
                
                if not invariant:
                    is_char = False
                    break
            
            neg_q_ok = not is_char
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1