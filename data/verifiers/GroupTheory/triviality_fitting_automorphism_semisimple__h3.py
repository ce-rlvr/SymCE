import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

def is_semisimple(G):
    """
    A finite group is a direct product of simple groups (semisimple) 
    iff every normal subgroup has a normal complement.
    """
    elements = list(G.elements)
    if len(elements) == 1:
        return True
        
    classes = []
    visited = set()
    for g in elements:
        if g in visited:
            continue
        c = set([g])
        q = [g]
        while q:
            curr = q.pop(0)
            for gen in G.generators:
                conj = ~gen * curr * gen
                if conj not in c:
                    c.add(conj)
                    q.append(conj)
        classes.append(list(c))
        visited.update(c)
        
    closures = []
    for i in range(len(classes)):
        subset = set(classes[i])
        q = list(subset)
        closure = set(subset)
        while q:
            curr = q.pop(0)
            for x in subset:
                prod = curr * x
                if prod not in closure:
                    closure.add(prod)
                    q.append(prod)
        closures.append(closure)
        
    ns_set = set([frozenset(c) for c in closures])
    ns_set.add(frozenset([G.identity]))
    
    q = list(closures)
    while q:
        curr = q.pop(0)
        for c in closures:
            prod = set()
            for x in curr:
                for y in c:
                    prod.add(x * y)
            fs = frozenset(prod)
            if fs not in ns_set:
                ns_set.add(fs)
                q.append(prod)
                
    G_set = frozenset(elements)
    for N in ns_set:
        has_complement = False
        for M in ns_set:
            if len(N.intersection(M)) == 1:
                if len(N) * len(M) == len(G_set):
                    has_complement = True
                    break
        if not has_complement:
            return False
    return True

def get_automorphism_group(G):
    elements = list(G.elements)
    n = len(elements)
    if n == 1:
        return PermutationGroup([Permutation(0)])
        
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    gens = G.generators
    gen_orders = [g.order() for g in gens]
    candidates = []
    for order in gen_orders:
        cands = [e for e in elements if e.order() == order]
        candidates.append(cands)
        
    automorphisms = []
    for p in itertools.product(*candidates):
        mapping = {G.identity: G.identity}
        valid = True
        q = [G.identity]
        
        while q:
            curr = q.pop(0)
            for i, gen in enumerate(gens):
                nxt = curr * gen
                nxt_img = mapping[curr] * p[i]
                if nxt in mapping:
                    if mapping[nxt] != nxt_img:
                        valid = False
                        break
                else:
                    mapping[nxt] = nxt_img
                    q.append(nxt)
            if not valid:
                break
                
        if valid and len(mapping) == n:
            if len(set(mapping.values())) == n:
                automorphisms.append(mapping)
                
    perms = []
    for mapping in automorphisms:
        p_arr = [0] * n
        for i, e in enumerate(elements):
            p_arr[i] = elem_to_idx[mapping[e]]
        perms.append(Permutation(p_arr))
        
    if not perms:
        return PermutationGroup([Permutation(n-1)])
    return PermutationGroup(perms)

def get_fitting_subgroup_order(H):
    elements = list(H.elements)
    if len(elements) == 1:
        return 1
        
    classes = []
    visited = set()
    for g in elements:
        if g in visited:
            continue
        c = set([g])
        q = [g]
        while q:
            curr = q.pop(0)
            for gen in H.generators:
                conj = ~gen * curr * gen
                if conj not in c:
                    c.add(conj)
                    q.append(conj)
        classes.append(list(c))
        visited.update(c)
        
    closures = []
    for i in range(len(classes)):
        subset = set(classes[i])
        q = list(subset)
        closure = set(subset)
        while q:
            curr = q.pop(0)
            for x in subset:
                prod = curr * x
                if prod not in closure:
                    closure.add(prod)
                    q.append(prod)
        closures.append(closure)
        
    ns_set = set([frozenset(c) for c in closures])
    ns_set.add(frozenset([H.identity]))
    
    q = list(closures)
    while q:
        curr = q.pop(0)
        for c in closures:
            prod = set()
            for x in curr:
                for y in c:
                    prod.add(x * y)
            fs = frozenset(prod)
            if fs not in ns_set:
                ns_set.add(fs)
                q.append(prod)
                
    def get_gens(elements_set):
        gens = []
        current_subgroup = set([H.identity])
        for e in elements_set:
            if e not in current_subgroup:
                gens.append(e)
                q_sub = list(current_subgroup)
                while q_sub:
                    curr = q_sub.pop(0)
                    for g in gens:
                        prod = curr * g
                        if prod not in current_subgroup:
                            current_subgroup.add(prod)
                            q_sub.append(prod)
                if len(current_subgroup) == len(elements_set):
                    break
        return gens

    max_nilpotent_order = 1
    for ns in ns_set:
        if len(ns) > max_nilpotent_order:
            gens = get_gens(ns)
            if not gens:
                continue
            subgrp = PermutationGroup(gens)
            if subgrp.is_nilpotent:
                max_nilpotent_order = len(ns)
                
    return max_nilpotent_order

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup) and witness.order() < float('inf')
    except Exception:
        h1 = False
        
    try:
        h2 = is_semisimple(witness)
    except Exception:
        h2 = False
        
    try:
        aut_G = get_automorphism_group(witness)
        fit_order = get_fitting_subgroup_order(aut_G)
        neg_q = fit_order > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "¬Q: The Fitting subgroup of Aut(G) is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2