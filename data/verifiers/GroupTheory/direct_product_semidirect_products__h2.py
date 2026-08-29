import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(G, H):
    try:
        G_elems = set(G.generate())
        for h in H.generators:
            if h not in G_elems:
                return False
        return True
    except Exception:
        return False

def is_normal(G, N):
    try:
        if not is_subgroup(G, N): 
            return False
        N_elems = set(N.generate())
        for g in G.generators:
            g_inv = ~g
            for n in N.generators:
                if g * n * g_inv not in N_elems:
                    return False
        return True
    except Exception:
        return False

def trivial_intersection(N, H):
    try:
        N_elems = set(N.generate())
        H_elems = set(H.generate())
        intersection = N_elems.intersection(H_elems)
        return len(intersection) == 1
    except Exception:
        return False

def normalizes(H, N):
    try:
        N_elems = set(N.generate())
        for h in H.generators:
            h_inv = ~h
            for n in N.generators:
                if h * n * h_inv not in N_elems:
                    return False
        return True
    except Exception:
        return False

def direct_product(G1, G2):
    deg1 = G1.degree
    deg2 = G2.degree
    perms = []
    for p in G1.generators:
        a = list(p.array_form)
        if len(a) < deg1:
            a += list(range(len(a), deg1))
        a += list(range(deg1, deg1 + deg2))
        perms.append(Permutation(a))
    for p in G2.generators:
        a = list(range(deg1))
        p_arr = list(p.array_form)
        if len(p_arr) < deg2:
            p_arr += list(range(len(p_arr), deg2))
        a += [x + deg1 for x in p_arr]
        perms.append(Permutation(a))
    if not perms:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(perms)

def get_sdp_permutations(N1, H1, N2, H2):
    N1_elems = list(N1.generate())
    H1_elems = list(H1.generate())
    N2_elems = list(N2.generate())
    H2_elems = list(H2.generate())
    
    elements = []
    for n1 in N1_elems:
        for n2 in N2_elems:
            for h1 in H1_elems:
                for h2 in H2_elems:
                    elements.append((n1, n2, h1, h2))
                    
    elem_to_idx = {elem: i for i, elem in enumerate(elements)}
    
    act1_map = {}
    for h1 in H1_elems:
        h1_inv = ~h1
        for n1 in N1_elems:
            act1_map[(h1, n1)] = h1 * n1 * h1_inv
            
    act2_map = {}
    for h2 in H2_elems:
        h2_inv = ~h2
        for n2 in N2_elems:
            act2_map[(h2, n2)] = h2 * n2 * h2_inv
            
    mult_n1 = { (a, b): a * b for a in N1_elems for b in N1_elems }
    mult_n2 = { (a, b): a * b for a in N2_elems for b in N2_elems }
    mult_h1 = { (a, b): a * b for a in H1_elems for b in H1_elems }
    mult_h2 = { (a, b): a * b for a in H2_elems for b in H2_elems }

    perms = []
    for g in elements:
        gn1, gn2, gh1, gh2 = g
        p = []
        for x in elements:
            xn1, xn2, xh1, xh2 = x
            act1 = act1_map[(gh1, xn1)]
            act2 = act2_map[(gh2, xn2)]
            
            new_n1 = mult_n1.get((gn1, act1))
            new_n2 = mult_n2.get((gn2, act2))
            new_h1 = mult_h1.get((gh1, xh1))
            new_h2 = mult_h2.get((gh2, xh2))
            
            if new_n1 is None or new_n2 is None:
                return None
                
            new_elem = (new_n1, new_n2, new_h1, new_h2)
            p.append(elem_to_idx[new_elem])
        perms.append(Permutation(p))
        
    if not perms:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(perms)

def conditions(witness):
    """
    witness is expected to be a tuple: (G1, N1, H1, G2, N2, H2)
    """
    try:
        G1, N1, H1, G2, N2, H2 = witness
    except Exception:
        return [False, False]
        
    # H_1: G1 = N1 \rtimes H1
    try:
        h1_ok = (is_normal(G1, N1) and 
                 is_subgroup(G1, H1) and 
                 trivial_intersection(N1, H1) and 
                 (N1.order() * H1.order() == G1.order()))
    except Exception:
        h1_ok = False
        
    # neg_Q: G1 x G2 is NOT isomorphic to (N1 x N2) \rtimes (H1 x H2)
    try:
        if not is_subgroup(G2, N2) or not is_subgroup(G2, H2):
            neg_q = True
        elif not normalizes(H2, N2):
            neg_q = True
        else:
            DP = direct_product(G1, G2)
            SDP = get_sdp_permutations(N1, H1, N2, H2)
            
            if SDP is None:
                neg_q = True
            elif DP.order() != SDP.order():
                neg_q = True
            else:
                neg_q = not DP.is_isomorphic(SDP)
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G_1 = N_1 \\rtimes_{\\phi_1} H_1 is a semidirect product",
    "¬Q: G_1 x G_2 is not isomorphic to (N_1 x N_2) \\rtimes (H_1 x H_2)"
]

N_HYP = 1
NEG_Q_INDEX = 1