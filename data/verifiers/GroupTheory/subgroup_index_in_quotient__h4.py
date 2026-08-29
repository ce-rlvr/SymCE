import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def resize_perm(p, size):
    arr = p.array_form
    if len(arr) == size:
        return p
    elif len(arr) < size:
        return Permutation(arr + list(range(len(arr), size)))
    else:
        return Permutation(arr[:size])

def group_contains(G, p):
    if p.size > G.degree:
        for i in range(G.degree, p.size):
            if p(i) != i:
                return False
    p_res = resize_perm(p, G.degree)
    return p_res in G

def is_subgroup(H, G):
    try:
        if not isinstance(H, PermutationGroup): return False
        if not isinstance(G, PermutationGroup): return False
        for gen in H.generators:
            if not group_contains(G, gen):
                return False
        return True
    except Exception:
        return False

def is_normal(N, G):
    try:
        if not is_subgroup(N, G): return False
        for g in G.generators:
            for n in N.generators:
                max_deg = max(g.size, n.size, G.degree, N.degree)
                g_res = resize_perm(g, max_deg)
                n_res = resize_perm(n, max_deg)
                g_inv_res = ~g_res
                conj1 = g_res * n_res * g_inv_res
                conj2 = g_inv_res * n_res * g_res
                if not group_contains(N, conj1):
                    return False
                if not group_contains(N, conj2):
                    return False
        return True
    except Exception:
        return False

def get_order(G):
    order = G.order
    if callable(order):
        return order()
    return order

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    h2 = is_normal(N, G)

    # H_3: H is a subgroup of G
    h3 = is_subgroup(H, G)

    # neg_Q: The index of H in G is not equal to the index of H/N in G/N
    try:
        order_G = get_order(G)
        order_H = get_order(H)
        index_GH = order_G // order_H
        
        max_deg = max(G.degree, H.degree, N.degree)
        H_gens = [resize_perm(gen, max_deg) for gen in H.generators]
        N_gens = [resize_perm(gen, max_deg) for gen in N.generators]
        
        HN_gens = H_gens + N_gens
        if not HN_gens:
            HN_gens = [Permutation(max_deg - 1)] if max_deg > 0 else [Permutation(0)]
        HN = PermutationGroup(HN_gens)
            
        order_HN = get_order(HN)
        index_G_HN = order_G // order_HN
        neg_q = bool(index_GH != index_G_HN)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "¬Q: The index of H in G is not equal to the index of H/N in G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3