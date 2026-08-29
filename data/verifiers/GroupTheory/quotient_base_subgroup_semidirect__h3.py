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

def get_intersection_order(G1, G2):
    """Safely compute the order of the intersection of two permutation groups."""
    try:
        if hasattr(G1, 'intersection'):
            return G1.intersection(G2).order()
        elif hasattr(G1, 'intersect'):
            return G1.intersect(G2).order()
    except Exception:
        pass
    
    # Fallback to element iteration for groups where intersection method is missing
    if G1.order() < G2.order():
        small, large = G1, G2
    else:
        small, large = G2, G1
    
    count = 0
    for g in small.elements:
        if g in large:
            count += 1
    return count

def conditions(witness) -> list[bool]:
    try:
        G, N, H, K = witness
    except Exception:
        return [False] * 5 + [False]
        
    # H_1: G is a group
    try:
        h1 = hasattr(G, 'order') and hasattr(G, 'generators')
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # H_3: G is the internal semidirect product of N and H
    try:
        h3 = (N.is_normal(G) and 
              H.is_subgroup(G) and 
              (get_intersection_order(N, H) == 1) and 
              (N.order() * H.order() == G.order()))
    except Exception:
        h3 = False
        
    # H_4: K is a normal subgroup of G
    try:
        h4 = K.is_subgroup(G) and K.is_normal(G)
    except Exception:
        h4 = False
        
    # H_5: K is a subgroup of N
    try:
        h5 = K.is_subgroup(N)
    except Exception:
        h5 = False
        
    # ¬Q: G/K is NOT isomorphic to the internal semidirect product of N/K and HK/K
    try:
        if not (K.is_subgroup(N) and K.is_subgroup(G)):
            Q = False
        else:
            HK_gen = PermutationGroup(list(H.generators) + list(K.generators))
            
            if not HK_gen.is_subgroup(G):
                Q = False
            else:
                # Check if the set HK is actually a subgroup
                H_int_K_order = get_intersection_order(H, K)
                set_HK_size = (H.order() * K.order()) // H_int_K_order
                is_HK_subgroup = (HK_gen.order() == set_HK_size)
                
                # Check if quotients N/K and HK/K are well-defined
                is_K_normal_in_N = K.is_normal(N)
                is_K_normal_in_HK = K.is_normal(HK_gen)
                
                # Check internal semidirect product properties in G/K
                int_N_HK_order = get_intersection_order(N, HK_gen)
                is_intersection_trivial = (int_N_HK_order == K.order())
                
                order_N_K = N.order() // K.order()
                order_HK_K = HK_gen.order() // K.order()
                order_G_K = G.order() // K.order()
                is_product_full = (order_N_K * order_HK_K == order_G_K)
                
                is_N_K_normal = N.is_normal(G)
                
                Q = (is_HK_subgroup and 
                     is_K_normal_in_N and 
                     is_K_normal_in_HK and 
                     is_intersection_trivial and 
                     is_product_full and 
                     is_N_K_normal)
        neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "H_4: K is a normal subgroup of G",
    "H_5: K is a subgroup of N",
    "¬Q: G/K is not isomorphic to the internal semidirect product of N/K and HK/K"
]

N_HYP = 5
NEG_Q_INDEX = 5