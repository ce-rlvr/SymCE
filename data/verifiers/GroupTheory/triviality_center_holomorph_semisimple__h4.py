import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
trivial = PermutationGroup(Permutation(0))

def is_semisimple(G):
    """
    A finite group is semisimple (completely reducible) if it is a direct product of simple groups.
    This is equivalent to every normal subgroup having a normal complement.
    """
    normal_subgroups = G.normal_subgroups()
    order_G = G.order()
    for N in normal_subgroups:
        has_complement = False
        for K in normal_subgroups:
            if N.order() * K.order() == order_G:
                # If |N| * |K| == |G| and N, K are normal, they are complements iff |NK| == |G|
                NK = PermutationGroup(N.generators + K.generators)
                if NK.order() == order_G:
                    has_complement = True
                    break
        if not has_complement:
            return False
    return True

def center_of_hol_is_trivial(G):
    """
    The center of Hol(G) is isomorphic to the subgroup of elements in Z(G) 
    that are fixed by all automorphisms of G.
    """
    elements = list(G.generate())
    n = len(elements)
    if n == 1:
        return True
        
    elem_to_idx = {g: i for i, g in enumerate(elements)}
        
    gens = G.generators
    center_indices = []
    for i, g in enumerate(elements):
        is_center = True
        for gen in gens:
            if g * gen != gen * g:
                is_center = False
                break
        if is_center:
            center_indices.append(i)
            
    if len(center_indices) == 1:
        return True
        
    id_elem = None
    for g in elements:
        if getattr(g, 'is_Identity', False):
            id_elem = g
            break
    if id_elem is None:
        for g in elements:
            if g.order() == 1:
                id_elem = g
                break
                
    id_idx = elem_to_idx[id_elem]
    
    mult = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            prod = elements[i] * elements[j]
            mult[i][j] = elem_to_idx[prod]
            
    gen_indices = [elem_to_idx[g] for g in gens]
    orders = [g.order() for g in elements]
    
    automorphisms = []
    
    def backtrack(gen_idx, current_mapping):
        if gen_idx == len(gen_indices):
            full_map = [-1] * n
            full_map[id_idx] = id_idx
            for gi, target in zip(gen_indices, current_mapping):
                full_map[gi] = target
                
            q = [id_idx]
            head = 0
            while head < len(q):
                u = q[head]
                head += 1
                for gi in gen_indices:
                    v = mult[u][gi]
                    mapped_v = mult[full_map[u]][full_map[gi]]
                    if full_map[v] == -1:
                        full_map[v] = mapped_v
                        q.append(v)
                    elif full_map[v] != mapped_v:
                        return 
                        
            if -1 not in full_map and len(set(full_map)) == n:
                valid = True
                for i in range(n):
                    for j in range(n):
                        if full_map[mult[i][j]] != mult[full_map[i]][full_map[j]]:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    automorphisms.append(full_map)
            return

        g = gen_indices[gen_idx]
        req_order = orders[g]
        for i in range(n):
            if orders[i] == req_order:
                backtrack(gen_idx + 1, current_mapping + [i])

    backtrack(0, [])
    
    for idx in center_indices:
        if idx == id_idx:
            continue
        fixed_by_all = True
        for aut in automorphisms:
            if aut[idx] != idx:
                fixed_by_all = False
                break
        if fixed_by_all:
            return False
            
    return True

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = is_semisimple(witness)
    except Exception:
        h2 = False
        
    try:
        h3 = witness.order() > 1
    except Exception:
        h3 = False
        
    try:
        neg_q = not center_of_hol_is_trivial(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: G is a non-trivial group",
    "¬Q: The center of Hol(G) is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3