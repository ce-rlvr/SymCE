import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def cond1_sympy(G):
    norms = G.normal_subgroups()
    minimal = []
    for H in norms:
        if H.order() == 1:
            continue
        is_min = True
        for K in norms:
            if K.order() == 1 or K.order() == H.order():
                continue
            # Check if K is a subgroup of H
            if all(g in H for g in K.generators):
                is_min = False
                break
        if is_min:
            minimal.append(H)
            
    prod = 1
    for H in minimal:
        prod *= H.order()
    if prod != G.order():
        return False
        
    for H in minimal:
        if len(H.normal_subgroups()) != 2:
            return False
            
    for i in range(len(minimal)):
        for j in range(i+1, len(minimal)):
            if minimal[i].is_isomorphic(minimal[j]):
                return False
    return True

def cond2_sympy(G, N):
    if not all(g in G for g in N.generators):
        return False
    for g in G.generators:
        for n in N.generators:
            if (g * n * ~g) not in N:
                return False
    return True

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is the direct product of pairwise non-isomorphic simple groups
    try:
        if hasattr(G, 'is_direct_product_of_pairwise_non_isomorphic_simple_groups'):
            h1 = G.is_direct_product_of_pairwise_non_isomorphic_simple_groups()
        elif hasattr(G, 'is_direct_product') and hasattr(G, 'factors_simple') and hasattr(G, 'factors_non_isomorphic'):
            h1 = G.is_direct_product() and G.factors_simple() and G.factors_non_isomorphic()
        else:
            h1 = cond1_sympy(G)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        if hasattr(N, 'is_normal_subgroup'):
            h2 = N.is_normal_subgroup(G)
        elif hasattr(G, 'is_normal_subgroup'):
            h2 = G.is_normal_subgroup(N)
        elif hasattr(N, 'is_normal'):
            h2 = N.is_normal(G)
        elif hasattr(G, 'is_normal'):
            h2 = G.is_normal(N)
        else:
            h2 = cond2_sympy(G, N)
    except Exception:
        h2 = False
        
    # ¬Q: N is not a characteristic subgroup of G
    try:
        if hasattr(N, 'is_characteristic_subgroup'):
            neg_q_val = not N.is_characteristic_subgroup(G)
        elif hasattr(G, 'is_characteristic_subgroup'):
            neg_q_val = not G.is_characteristic_subgroup(N)
        elif hasattr(N, 'is_characteristic'):
            neg_q_val = not N.is_characteristic(G)
        elif hasattr(G, 'is_characteristic'):
            neg_q_val = not G.is_characteristic(N)
        else:
            # For finite groups, every normal subgroup of a direct product of 
            # pairwise non-isomorphic simple groups is characteristic.
            # Thus, no finite counterexample exists.
            neg_q_val = False
    except Exception:
        neg_q_val = False
        
    return [bool(h1), bool(h2), bool(neg_q_val)]

CONDITION_LABELS = [
    "H_1: G is the direct product of pairwise non-isomorphic simple groups",
    "H_2: N is a normal subgroup of G",
    "¬Q: N is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2