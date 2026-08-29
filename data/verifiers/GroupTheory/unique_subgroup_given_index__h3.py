import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def conditions(witness):
    try:
        G, H, n = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group and H is a subgroup of G
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
            h1 = False
        else:
            try:
                h1 = bool(H.is_subgroup(G))
            except Exception:
                elements_G = set(G.generate())
                h1 = bool(all(g in elements_G for g in H.generators))
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = bool((isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 0)
    except Exception:
        h2 = False

    # H_3: For any subgroup K of G, if index of K in G is n, then K = H
    try:
        h3 = True
        if h1 and h2:
            order_G = G.order()
            if order_G % n != 0:
                h3 = True
            else:
                target_order = order_G // n
                H_set = set(H.generate())
                
                index_n_subgroups = []
                try:
                    subs = G.subgroups()
                    for sub in subs:
                        if sub.order() == target_order:
                            index_n_subgroups.append(set(sub.generate()))
                except Exception:
                    elements = list(G.generate())
                    id_elem = G.identity
                    
                    cyclic_subgroups = set()
                    for g in elements:
                        H_g = set([id_elem])
                        curr = g
                        while curr != id_elem:
                            H_g.add(curr)
                            curr = curr * g
                        cyclic_subgroups.add(frozenset(H_g))
                    
                    all_subgroups = set(cyclic_subgroups)
                    queue = list(cyclic_subgroups)
                    
                    for sub in queue:
                        for C in cyclic_subgroups:
                            generators = list(sub | C)
                            closure = frozenset(PermutationGroup(generators).generate())
                            if closure not in all_subgroups:
                                all_subgroups.add(closure)
                                queue.append(closure)
                    
                    for sub in all_subgroups:
                        if len(sub) == target_order:
                            index_n_subgroups.append(sub)
                
                for K in index_n_subgroups:
                    if K != H_set:
                        h3 = False
                        break
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: H is not a normal subgroup of G
    try:
        if h1:
            neg_q = not H.is_normal(G)
        else:
            neg_q = False
    except Exception:
        try:
            if h1:
                elements_G = list(G.generate())
                elements_H = set(H.generate())
                is_normal = True
                for g in elements_G:
                    g_inv = ~g
                    for h in elements_H:
                        if (g * h * g_inv) not in elements_H:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
            else:
                neg_q = False
        except Exception:
            neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and H is a subgroup of G",
    "H_2: n is a positive integer",
    "H_3: For any subgroup K of G, if index of K in G is n, then K = H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3