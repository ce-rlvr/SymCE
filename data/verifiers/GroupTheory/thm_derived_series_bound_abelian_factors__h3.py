import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation()])

def robust_contains(G, p):
    try:
        if p in G:
            return True
    except Exception:
        pass
    
    try:
        degree = G.degree
        p_size = p.size
        if p_size < degree:
            arr = p.array_form + list(range(p_size, degree))
            p_new = Permutation(arr)
            return p_new in G
        elif p_size > degree:
            for i in range(degree, p_size):
                if p(i) != i:
                    return False
            arr = p.array_form[:degree]
            p_new = Permutation(arr)
            return p_new in G
    except Exception:
        pass
    return False

def is_subgroup(G, H):
    for h in H.generators:
        if not robust_contains(G, h):
            return False
    return True

def is_normal_subgroup(G, H):
    if not is_subgroup(G, H):
        return False
    for g in G.generators:
        for h in H.generators:
            max_size = max(g.size, h.size)
            g_arr = g.array_form + list(range(g.size, max_size))
            h_arr = h.array_form + list(range(h.size, max_size))
            g_pad = Permutation(g_arr)
            h_pad = Permutation(h_arr)
            conj = g_pad * h_pad * ~g_pad
            if not robust_contains(H, conj):
                return False
    return True

def is_trivial(G):
    return G.order() == 1

def derived_series_term(G, n):
    curr = G
    for _ in range(n):
        if hasattr(curr, 'derived_subgroup'):
            curr = curr.derived_subgroup()
        else:
            break
    return curr

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G_obj, n_val = witness
            if hasattr(G_obj, 'generators') and hasattr(G_obj, 'degree') and n_val == 1:
                witness = [G_obj, PermutationGroup([Permutation()])]
        elif hasattr(witness, 'generators') and hasattr(witness, 'degree'):
            witness = [witness, PermutationGroup([Permutation()])]
    except Exception:
        pass

    try:
        h1 = False
        if isinstance(witness, list) and len(witness) >= 2:
            h1 = all(hasattr(g, 'generators') and hasattr(g, 'degree') for g in witness)
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if h1:
            if is_trivial(witness[-1]):
                is_subnormal = True
                for i in range(len(witness) - 1):
                    G_i = witness[i]
                    G_next = witness[i+1]
                    if not is_normal_subgroup(G_i, G_next):
                        is_subnormal = False
                        break
                    if G_i.order() <= G_next.order():
                        is_subnormal = False
                        break
                h2 = is_subnormal
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        if h1:
            n = len(witness) - 1
            G_0 = witness[0]
            Gn = derived_series_term(G_0, n)
            neg_q = not is_trivial(Gn)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: G possesses a subnormal series of length n", "not Q: G^(n) is not trivial"]
N_HYP = 2
NEG_Q_INDEX = 2