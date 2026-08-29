import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def is_power_of_p(n, p):
    if n == 1: return True
    if p <= 1: return n == 1
    if n % p != 0: return False
    while n % p == 0:
        n //= p
    return n == 1

def highest_power_dividing(n, p):
    if p <= 1:
        return 1
    k = 0
    while n % (p**(k+1)) == 0:
        k += 1
    return p**k

def get_all_subgroups(G):
    elements = list(G.generate())
    if not elements:
        return set()
    
    id_elem = elements[0]
    for e in elements:
        if e * e == e:
            id_elem = e
            break
            
    subgroups = {frozenset([id_elem])}
    queue = [frozenset([id_elem])]
    
    while queue:
        current = queue.pop(0)
        for g in elements:
            if g not in current:
                new_sub = set(current)
                frontier = {g}
                new_sub.add(g)
                while frontier:
                    next_frontier = set()
                    for f in frontier:
                        for s in list(new_sub):
                            c1 = f * s
                            if c1 not in new_sub:
                                new_sub.add(c1)
                                next_frontier.add(c1)
                            c2 = s * f
                            if c2 not in new_sub:
                                new_sub.add(c2)
                                next_frontier.add(c2)
                    frontier = next_frontier
                
                new_sub_frozen = frozenset(new_sub)
                if new_sub_frozen not in subgroups:
                    subgroups.add(new_sub_frozen)
                    queue.append(new_sub_frozen)
                    
    return subgroups

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, p, S = witness
        p = int(p)
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'is_group') and G.is_group and hasattr(G, 'order')
        if h1:
            order = G.order()
            h1 = (order < float('inf'))
    except Exception:
        h1 = False

    # Precompute all subgroups if H1 holds to avoid redundant work
    try:
        if h1:
            all_subs = get_all_subgroups(G)
        else:
            all_subs = set()
    except Exception:
        all_subs = set()
        h1 = False

    # H_2: S is the set of all Sylow p-subgroups of G
    try:
        if not h1:
            h2 = False
        else:
            S_sets = []
            for H in S:
                S_sets.append(frozenset(H.generate()))
                
            # Definition 1: maximal p-subgroups
            p_subs = [sub for sub in all_subs if is_power_of_p(len(sub), p)]
            maximal_p_subs = []
            for sub in p_subs:
                is_maximal = True
                for other in p_subs:
                    if len(sub) < len(other) and sub.issubset(other):
                        is_maximal = False
                        break
                if is_maximal:
                    maximal_p_subs.append(sub)
                    
            match1 = (len(maximal_p_subs) == len(S_sets) and all(s in maximal_p_subs for s in S_sets))
            
            # Definition 2: subgroups of order highest_power_dividing(|G|, p)
            target_order = highest_power_dividing(G.order(), p)
            def2_subs = [sub for sub in all_subs if len(sub) == target_order]
            match2 = (len(def2_subs) == len(S_sets) and all(s in def2_subs for s in S_sets))
            
            h2 = match1 or match2
    except Exception:
        h2 = False

    # ¬Q: The intersection of all subgroups in S is NOT the unique largest normal p-subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            if not S:
                intersect = frozenset(G.generate())
            else:
                S_sets = [frozenset(H.generate()) for H in S]
                intersect = set(S_sets[0])
                for s in S_sets[1:]:
                    intersect = intersect.intersection(s)
                intersect = frozenset(intersect)
            
            normal_p_subs = []
            generators = list(G.generators)
            for sub in all_subs:
                if is_power_of_p(len(sub), p):
                    is_normal = True
                    for g in generators:
                        g_inv = g**-1
                        for h in sub:
                            if g * h * g_inv not in sub:
                                is_normal = False
                                break
                        if not is_normal:
                            break
                    if is_normal:
                        normal_p_subs.append(sub)
                        
            Op = None
            for sub in normal_p_subs:
                contains_all = True
                for other in normal_p_subs:
                    if not other.issubset(sub):
                        contains_all = False
                        break
                if contains_all:
                    Op = sub
                    break
                    
            if Op is None:
                neg_q = True
            else:
                neg_q = (intersect != Op)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: S is the set of all Sylow p-subgroups of G",
    "¬Q: The intersection of all subgroups in S is NOT the unique largest normal p-subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2