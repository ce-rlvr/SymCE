import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.ntheory import factorint

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3))
trivial = CyclicGroup(1)

def is_cyclic(G):
    order = G.order()
    if order == 1:
        return True
    prime_factors = list(factorint(order).keys())
    identity = G.identity
    for g in G.elements:
        generates = True
        for p in prime_factors:
            if (g**(order // p)) == identity:
                generates = False
                break
        if generates:
            return True
    return False

def is_semidirect_product(G, N, H):
    n_order = N.order()
    h_order = H.order()
    if G.order() != n_order * h_order:
        return False
    
    normal_subs = [sub for sub in G.normal_subgroups() if sub.order() == n_order]
    if not normal_subs:
        return False
        
    subs = [sub for sub in G.subgroups() if sub.order() == h_order]
    if not subs:
        return False
        
    for n_sub in normal_subs:
        if not n_sub.is_isomorphic(N):
            continue
        for h_sub in subs:
            if not h_sub.is_isomorphic(H):
                continue
            # check trivial intersection
            intersect_size = sum(1 for g in h_sub.elements if g in n_sub)
            if intersect_size == 1:
                return True
    return False

def is_metacyclic(G):
    for N in G.normal_subgroups():
        if is_cyclic(N):
            q_order = G.order() // N.order()
            if q_order == 1:
                return True
            prime_factors = list(factorint(q_order).keys())
            is_quotient_cyclic = False
            for g in G.elements:
                generates = True
                for p in prime_factors:
                    k = q_order // p
                    if (g**k) in N:
                        generates = False
                        break
                if generates:
                    if (g**q_order) in N:
                        is_quotient_cyclic = True
                        break
            if is_quotient_cyclic:
                return True
    return False

def conditions(witness):
    try:
        N, H, G = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_cyclic(N)
    except Exception:
        h1 = False
        
    try:
        h2 = is_semidirect_product(G, N, H)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_metacyclic(G)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a cyclic group",
    "H_2: G is an external semidirect product of N and H",
    "¬Q: G is not a metacyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2