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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def eval_f(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def get_elements(G):
    try:
        return list(G.elements)
    except Exception:
        return list(G.generate())

def get_identity(G):
    if hasattr(G, 'identity'):
        return G.identity
    for g in get_elements(G):
        if g * g == g:
            return g

def is_abelian(G):
    if hasattr(G, 'is_abelian'):
        return G.is_abelian
    elems = get_elements(G)
    for a in elems:
        for b in elems:
            if a * b != b * a:
                return False
    return True

def are_isomorphic(G1, G2):
    elems1 = get_elements(G1)
    elems2 = get_elements(G2)
    if len(elems1) != len(elems2):
        return False
    if is_abelian(G1) != is_abelian(G2):
        return False
    try:
        if hasattr(G1, 'is_isomorphic'):
            res = G1.is_isomorphic(G2)
            if res is not None:
                return res
    except Exception:
        pass
        
    if len(elems1) > 8:
        return False
        
    id1 = get_identity(G1)
    id2 = get_identity(G2)
    
    elems1_non_id = [g for g in elems1 if g != id1]
    elems2_non_id = [g for g in elems2 if g != id2]
    
    def get_order_el(g, id_el):
        ord = 1
        curr = g
        while curr != id_el:
            curr = curr * g
            ord += 1
        return ord
        
    orders1 = [get_order_el(g, id1) for g in elems1_non_id]
    orders2 = [get_order_el(g, id2) for g in elems2_non_id]
    
    if sorted(orders1) != sorted(orders2):
        return False
        
    for p in itertools.permutations(elems2_non_id):
        mapping = {id1: id2}
        valid = True
        for i, g1 in enumerate(elems1_non_id):
            g2 = p[i]
            if orders1[i] != get_order_el(g2, id2):
                valid = False
                break
            mapping[g1] = g2
        if not valid:
            continue
            
        is_homo = True
        for a in elems1:
            for b in elems1:
                if mapping[a * b] != mapping[a] * mapping[b]:
                    is_homo = False
                    break
            if not is_homo:
                break
        if is_homo:
            return True
    return False

def get_subgroups(G):
    elements = get_elements(G)
    id_el = get_identity(G)
    subgroups = {frozenset([id_el])}
    
    for g in elements:
        cyc = [id_el]
        curr = g
        while curr != id_el:
            if curr not in cyc:
                cyc.append(curr)
            curr = curr * g
        subgroups.add(frozenset(cyc))
        
    added = True
    while added:
        added = False
        current_subs = list(subgroups)
        for i in range(len(current_subs)):
            for j in range(i + 1, len(current_subs)):
                S1 = current_subs[i]
                S2 = current_subs[j]
                new_sub = set(S1 | S2)
                changed = True
                while changed:
                    changed = False
                    prods = set()
                    for a in new_sub:
                        for b in new_sub:
                            prods.add(a * b)
                    if not prods.issubset(new_sub):
                        new_sub.update(prods)
                        changed = True
                new_sub_fs = frozenset(new_sub)
                if new_sub_fs not in subgroups:
                    subgroups.add(new_sub_fs)
                    added = True
    return subgroups

def make_group(elements_set):
    return PermutationGroup(list(elements_set))

def neg_conclusion(G, H, f):
    id_H = get_identity(H)
    ker_f_elements = set()
    for g in get_elements(G):
        if eval_f(f, g) == id_H:
            ker_f_elements.add(g)
            
    subgroups = get_subgroups(G)
    
    normal_subgroups = []
    for sub in subgroups:
        is_normal = True
        for n in sub:
            for g in get_elements(G):
                if (g * n * ~g) not in sub:
                    is_normal = False
                    break
            if not is_normal:
                break
        if is_normal:
            normal_subgroups.append(sub)
            
    ker_f_group = make_group(ker_f_elements)
    
    N_candidates = []
    for N_set in normal_subgroups:
        if len(N_set) == len(ker_f_elements):
            N_grp = make_group(N_set)
            if are_isomorphic(N_grp, ker_f_group):
                N_candidates.append(N_set)
                
    M_candidates = []
    H_order = len(get_elements(H))
    for M_set in subgroups:
        if len(M_set) == H_order:
            M_grp = make_group(M_set)
            if are_isomorphic(M_grp, H):
                M_candidates.append(M_set)
                
    id_G = get_identity(G)
    has_complement = False
    for N_set in N_candidates:
        for M_set in M_candidates:
            if N_set.intersection(M_set) == {id_G}:
                has_complement = True
                break
        if has_complement:
            break
            
    return not has_complement

def conditions(witness):
    try:
        G, H, f = witness
    except Exception:
        return [False, False, False]
        
    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: f is a surjective group homomorphism
    try:
        h2 = False
        if h1:
            image = set()
            is_homo = True
            H_elems = get_elements(H)
            for g in get_elements(G):
                val = eval_f(f, g)
                if val not in H_elems:
                    is_homo = False
                    break
                image.add(val)
            if is_homo and len(image) == len(H_elems):
                for g1 in get_elements(G):
                    for g2 in get_elements(G):
                        if eval_f(f, g1 * g2) != eval_f(f, g1) * eval_f(f, g2):
                            is_homo = False
                            break
                    if not is_homo:
                        break
                h2 = is_homo
    except Exception:
        h2 = False
        
    # neg_Q: G is NOT isomorphic to the semidirect product of ker(f) and H
    try:
        neg_q = False
        if h1 and h2:
            neg_q = neg_conclusion(G, H, f)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a surjective group homomorphism",
    "¬Q: G is not isomorphic to the semidirect product of ker(f) and H"
]
N_HYP = 2
NEG_Q_INDEX = 2