import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

# Top-level setup for potential witness expressions
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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

def get_elements(obj):
    if hasattr(obj, 'elements'):
        return set(obj.elements)
    return set(obj)

def get_normal_subgroups(elements, id_elem):
    classes = []
    seen = set()
    for g in elements:
        if g not in seen:
            c = frozenset({x * g * ~x for x in elements})
            classes.append(c)
            seen.update(c)
            
    normal_subs = set()
    queue = [frozenset({id_elem})]
    visited = set(queue)
    
    while queue:
        curr = queue.pop(0)
        normal_subs.add(curr)
        for c in classes:
            if not c.issubset(curr):
                new_sub = set(curr)
                new_sub.update(c)
                while True:
                    size = len(new_sub)
                    new_sub.update({a * b for a in new_sub for b in new_sub})
                    if len(new_sub) == size:
                        break
                new_sub_fs = frozenset(new_sub)
                if new_sub_fs not in visited:
                    visited.add(new_sub_fs)
                    queue.append(new_sub_fs)
    return normal_subs

def is_supersolvable(elements, id_elem):
    if len(elements) == 1:
        return True
    normal_subs = get_normal_subgroups(elements, id_elem)
    normal_subs = sorted(list(normal_subs), key=len)
    
    def dfs(curr):
        if len(curr) == len(elements):
            return True
        for nxt in normal_subs:
            if len(nxt) > len(curr) and curr.issubset(nxt):
                if isprime(len(nxt) // len(curr)):
                    if dfs(nxt):
                        return True
        return False
    return dfs(frozenset({id_elem}))

def get_H_invariant_normal_subgroups_of_N(N_elements, H_elements, id_elem):
    G_elements = {n * h for n in N_elements for h in H_elements}
    classes = []
    seen = set()
    for g in N_elements:
        if g not in seen:
            c = frozenset({x * g * ~x for x in G_elements})
            classes.append(c)
            seen.update(c)
            
    inv_subs = set()
    queue = [frozenset({id_elem})]
    visited = set(queue)
    
    while queue:
        curr = queue.pop(0)
        inv_subs.add(curr)
        for c in classes:
            if not c.issubset(curr):
                new_sub = set(curr)
                new_sub.update(c)
                while True:
                    size = len(new_sub)
                    new_sub.update({a * b for a in new_sub for b in new_sub})
                    if len(new_sub) == size:
                        break
                new_sub_fs = frozenset(new_sub)
                if new_sub_fs not in visited:
                    visited.add(new_sub_fs)
                    queue.append(new_sub_fs)
    return inv_subs

def has_invariant_series(N_elements, H_elements, id_elem):
    inv_subs = get_H_invariant_normal_subgroups_of_N(N_elements, H_elements, id_elem)
    inv_subs = sorted(list(inv_subs), key=len)
    
    def dfs(curr):
        if len(curr) == len(N_elements):
            return True
        for nxt in inv_subs:
            if len(nxt) > len(curr) and curr.issubset(nxt):
                if isprime(len(nxt) // len(curr)):
                    if dfs(nxt):
                        return True
        return False
    return dfs(frozenset({id_elem}))

def is_semidirect_product(G_els, N_els, H_els, id_elem):
    if len(N_els.intersection(H_els)) != 1:
        return False
    if len(G_els) != len(N_els) * len(H_els):
        return False
    for n in N_els:
        for g in G_els:
            if g * n * ~g not in N_els:
                return False
    NH = {n * h for n in N_els for h in H_els}
    if NH != G_els:
        return False
    for h1 in H_els:
        for h2 in H_els:
            if h1 * h2 not in H_els:
                return False
    return True

def conditions(witness):
    try:
        G, N, H = witness
        G_els = get_elements(G)
        N_els = get_elements(N)
        H_els = get_elements(H)
        id_elem = list(G_els)[0] ** 0
        
        if not is_semidirect_product(G_els, N_els, H_els, id_elem):
            return [False, False, False]
            
        h1 = is_supersolvable(N_els, id_elem) and is_supersolvable(H_els, id_elem)
    except Exception:
        h1 = False
        
    try:
        h2 = has_invariant_series(N_els, H_els, id_elem)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_supersolvable(G_els, id_elem)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are supersolvable groups",
    "H_2: There exists a series of normal subgroups of N with prime cyclic quotient factors invariant under H",
    "¬Q: The semidirect product G is not a supersolvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2