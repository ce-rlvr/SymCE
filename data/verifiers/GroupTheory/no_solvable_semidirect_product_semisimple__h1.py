import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from itertools import combinations

# Top-level setup: named object bindings
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

def are_isomorphic(G1, G2):
    if G1.order() != G2.order():
        return False
    if bool(G1.is_abelian) != bool(G2.is_abelian):
        return False
        
    def element_orders(G):
        orders = {}
        for g in G.generate():
            o = g.order()
            orders[o] = orders.get(o, 0) + 1
        return orders
        
    if element_orders(G1) != element_orders(G2):
        return False
        
    try:
        if hasattr(G1, 'is_isomorphic'):
            return G1.is_isomorphic(G2)
    except Exception:
        pass
        
    return True

def get_normal_subgroups_of_order(G, target_order):
    try:
        elements = list(G.generate())
        classes = []
        seen = set()
        for x in elements:
            if x not in seen:
                c = set()
                for g in elements:
                    c.add(g * x * ~g)
                classes.append(list(c))
                seen.update(c)
                
        id_elem = G.identity
        other_classes = [c for c in classes if c[0] != id_elem]
        
        target_sum = target_order - 1
        
        def find_combinations(classes, target, current_combo, current_sum):
            if current_sum == target:
                yield current_combo
                return
            if current_sum > target or not classes:
                return
                
            c = classes[0]
            yield from find_combinations(classes[1:], target, current_combo + [c], current_sum + len(c))
            yield from find_combinations(classes[1:], target, current_combo, current_sum)
            
        normal_subgroups = []
        for combo in find_combinations(other_classes, target_sum, [], 0):
            elems = [id_elem]
            for c in combo:
                elems.extend(c)
                
            elems_set = set(elems)
            is_closed = True
            for x in elems:
                for y in elems:
                    if x * y not in elems_set:
                        is_closed = False
                        break
                if not is_closed:
                    break
            if is_closed:
                normal_subgroups.append(PermutationGroup(elems))
                
        return normal_subgroups
    except Exception:
        return []

def find_complement_subgroups(G, N_sub, H_order):
    try:
        elements = list(G.generate())
        N_elems = set(N_sub.generate())
        allowed = [x for x in elements if x not in N_elems]
        
        if H_order == 1:
            yield PermutationGroup([G.identity])
            return
            
        seen_subgroups = []
        
        def is_new(H_sub):
            H_sub_elems = set(H_sub.generate())
            for seen in seen_subgroups:
                if H_sub_elems == seen:
                    return False
            seen_subgroups.append(H_sub_elems)
            return True

        # Try 1-generated subgroups
        for x in allowed:
            H_sub = PermutationGroup([x])
            if H_sub.order() == H_order:
                if len(set(H_sub.generate()).intersection(N_elems)) == 1:
                    if is_new(H_sub):
                        yield H_sub
                    
        # Try 2-generated subgroups
        for i in range(len(allowed)):
            for j in range(i + 1, len(allowed)):
                H_sub = PermutationGroup([allowed[i], allowed[j]])
                if H_sub.order() == H_order:
                    if len(set(H_sub.generate()).intersection(N_elems)) == 1:
                        if is_new(H_sub):
                            yield H_sub
                        
        # Try 3-generated subgroups
        for i in range(len(allowed)):
            for j in range(i + 1, len(allowed)):
                for k in range(j + 1, len(allowed)):
                    H_sub = PermutationGroup([allowed[i], allowed[j], allowed[k]])
                    if H_sub.order() == H_order:
                        if len(set(H_sub.generate()).intersection(N_elems)) == 1:
                            if is_new(H_sub):
                                yield H_sub
    except Exception:
        pass

def check_H3(N, H, G):
    if not isinstance(G, PermutationGroup):
        return False
    if not isinstance(N, PermutationGroup):
        return False
    if not isinstance(H, PermutationGroup):
        return False
        
    # Case 1: N and H are already subgroups of G
    try:
        n_sub = all(gen in G for gen in N.generators)
        h_sub = all(gen in G for gen in H.generators)
        
        if n_sub and h_sub:
            n_normal = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        n_normal = False
                        break
                if not n_normal:
                    break
            
            if n_normal:
                n_elems = set(N.generate())
                h_elems = set(H.generate())
                if len(n_elems.intersection(h_elems)) == 1:
                    if N.order() * H.order() == G.order():
                        return True
    except Exception:
        pass

    # Case 2: N and H are abstract groups
    if N.order() * H.order() != G.order():
        return False
        
    if G.order() > 2000:
        return False
        
    normal_subs = get_normal_subgroups_of_order(G, N.order())
    for N_sub in normal_subs:
        if are_isomorphic(N_sub, N):
            for H_sub in find_complement_subgroups(G, N_sub, H.order()):
                if are_isomorphic(H_sub, H):
                    return True
                
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        N, H, G = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: N is a solvable group
    try:
        if not isinstance(N, PermutationGroup):
            h1 = False
        else:
            solvable = N.is_solvable
            if callable(solvable):
                h1 = bool(solvable())
            else:
                h1 = bool(solvable)
    except Exception:
        h1 = False
        
    # H_2: H is a group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False
        
    # H_3: G is isomorphic to the external semidirect product N \rtimes H
    try:
        h3 = check_H3(N, H, G)
    except Exception:
        h3 = False
        
    # neg_Q: N is not the trivial group
    try:
        neg_q = isinstance(N, PermutationGroup) and N.order() > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a solvable group",
    "H_2: H is a group",
    "H_3: G is isomorphic to the external semidirect product N \\rtimes H",
    "¬Q: N is not the trivial group"
]

N_HYP = 3
NEG_Q_INDEX = 3