import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup for potential witness expressions
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

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group (and N, H are groups)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of G
    try:
        if h1:
            h2 = set(H.elements).issubset(set(G.elements))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: G is the internal semidirect product of N and H
    try:
        if h1:
            n_elems = set(N.elements)
            h_elems = set(H.elements)
            g_elems = set(G.elements)
            
            n_is_sub = n_elems.issubset(g_elems)
            h_is_sub = h_elems.issubset(g_elems)
            
            # Check if N is a normal subgroup of G
            n_is_norm = True
            if n_is_sub:
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        if g * n * g_inv not in n_elems:
                            n_is_norm = False
                            break
                    if not n_is_norm:
                        break
            else:
                n_is_norm = False
                
            # Check trivial intersection and generation of G
            intersect_trivial = len(n_elems.intersection(h_elems)) == 1
            generates_G = len(n_elems) * len(h_elems) == len(g_elems)
            
            h3 = n_is_sub and n_is_norm and h_is_sub and intersect_trivial and generates_G
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: N_G(H) != C_N(H) ⋉ H
    try:
        if h1:
            h_elems = set(H.elements)
            
            # Compute N_G(H)
            ng_h = set()
            for g in G.elements:
                is_in_normalizer = True
                g_inv = ~g
                for h in H.generators:
                    if g * h * g_inv not in h_elems:
                        is_in_normalizer = False
                        break
                if is_in_normalizer:
                    ng_h.add(g)
                    
            # Compute C_N(H)
            cn_h = set()
            for n in N.elements:
                is_in_centralizer = True
                for h in H.generators:
                    if n * h != h * n:
                        is_in_centralizer = False
                        break
                if is_in_centralizer:
                    cn_h.add(n)
                    
            # Compute C_N(H) ⋉ H (which is just the set product C_N(H) * H)
            cn_h_h = set()
            for c in cn_h:
                for h in h_elems:
                    cn_h_h.add(c * h)
                    
            neg_q = ng_h != cn_h_h
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "¬Q: N_G(H) is not equal to the internal semidirect product of C_N(H) and H"
]

N_HYP = 3
NEG_Q_INDEX = 3