import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def get_all_subgroups(G):
    elements = list(G.generate())
    if not elements:
        return set()
    id_el = elements[0]**0
    
    def generate_subgroup(gens):
        S = {id_el}
        queue = [id_el]
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = curr * g
                if nxt not in S:
                    S.add(nxt)
                    queue.append(nxt)
        return frozenset(S)

    subgroups = {frozenset([id_el])}
    queue = [(frozenset([id_el]), [])]
    
    while queue:
        curr_S, curr_gens = queue.pop(0)
        for e in elements:
            if e not in curr_S:
                new_gens = curr_gens + [e]
                new_S = generate_subgroup(new_gens)
                if new_S not in subgroups:
                    subgroups.add(new_S)
                    queue.append((new_S, new_gens))
                    
    return subgroups

def is_characteristic(G, H_set):
    if not H_set:
        return False
    elements = list(G.generate())
    id_el = elements[0]**0
    
    # Check if H_set is a valid subgroup
    if id_el not in H_set:
        return False
    for a in H_set:
        for b in H_set:
            if a * b not in H_set:
                return False

    gens = G.generators
    
    def get_order(g):
        return g.order()

    gen_orders = [get_order(g) for g in gens]
    candidates = [ [e for e in elements if get_order(e) == o] for o in gen_orders ]
    
    for target_gens in itertools.product(*candidates):
        mapping = {id_el: id_el}
        queue = [id_el]
        is_hom = True
        
        while queue:
            curr = queue.pop(0)
            for i, g in enumerate(gens):
                nxt = curr * g
                mapped_nxt = mapping[curr] * target_gens[i]
                if nxt in mapping:
                    if mapping[nxt] != mapped_nxt:
                        is_hom = False
                        break
                else:
                    mapping[nxt] = mapped_nxt
                    queue.append(nxt)
            if not is_hom:
                break
                
        if is_hom and len(mapping) == len(elements) and len(set(mapping.values())) == len(elements):
            mapped_H = {mapping[h] for h in H_set}
            if mapped_H != H_set:
                return False
                
    return True

def conditions(witness):
    try:
        if len(witness) == 2:
            G, k = witness
            H = None
        elif len(witness) == 3:
            G, H, k = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = isinstance(k, int) and k > 0
    except Exception:
        h1_ok = False
        
    try:
        all_subgroups = get_all_subgroups(G)
        subgroups_of_order_k = [S for S in all_subgroups if len(S) == k]
        
        if H is not None:
            if hasattr(H, 'generate'):
                H_set = frozenset(list(H.generate()))
            else:
                H_set = frozenset(H)
            h2_ok = (len(subgroups_of_order_k) == 1) and (H_set in subgroups_of_order_k)
        else:
            h2_ok = (len(subgroups_of_order_k) == 1)
            if h2_ok:
                H_set = subgroups_of_order_k[0]
            else:
                H_set = None
    except Exception:
        h2_ok = False
        H_set = None
        
    try:
        if H_set is None:
            if H is not None:
                if hasattr(H, 'generate'):
                    H_set = frozenset(list(H.generate()))
                else:
                    H_set = frozenset(H)
                neg_q = not is_characteristic(G, H_set)
            else:
                neg_q = False
        else:
            neg_q = not is_characteristic(G, H_set)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "H_2: G contains exactly one subgroup H of order k",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2