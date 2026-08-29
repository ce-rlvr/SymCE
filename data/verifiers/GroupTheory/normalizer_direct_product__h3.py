import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def get_elements(X):
    if isinstance(X, PermutationGroup):
        return list(X.elements)
    return list(X)

def direct_product_elements(elems_A, elems_B, deg_G, deg_H):
    dp_elems = []
    for a in elems_A:
        for b in elems_B:
            arr = []
            for i in range(deg_G):
                arr.append(a(i))
            for i in range(deg_H):
                arr.append(b(i) + deg_G)
            dp_elems.append(Permutation(arr))
    return dp_elems

def normalizer_from_elems(group_elems, S_elems):
    S_set = set(S_elems)
    norm = []
    for g in group_elems:
        is_norm = True
        for s in S_set:
            if (g * s * ~g) not in S_set:
                is_norm = False
                break
        if is_norm:
            norm.append(g)
    return norm

def conditions(witness):
    try:
        G, H, A, B = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: A is a subgroup of G
    try:
        if isinstance(A, PermutationGroup):
            G_elems_set = set(G.elements)
            h3 = all(a in G_elems_set for a in A.elements)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The normalizer of A x B in G x H is NOT equal to N_G(A) x N_H(B)
    try:
        A_elems = get_elements(A)
        B_elems = get_elements(B)
        
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        
        deg_G = G.degree
        if A_elems:
            deg_G = max(deg_G, max(a.size for a in A_elems))
            
        deg_H = H.degree
        if B_elems:
            deg_H = max(deg_H, max(b.size for b in B_elems))
            
        AxB_elems = direct_product_elements(A_elems, B_elems, deg_G, deg_H)
        GxH_elems = direct_product_elements(G_elems, H_elems, deg_G, deg_H)
        
        N_GxH_AxB = normalizer_from_elems(GxH_elems, AxB_elems)
        
        N_G_A = normalizer_from_elems(G_elems, A_elems)
        N_H_B = normalizer_from_elems(H_elems, B_elems)
        
        N_G_A_x_N_H_B = direct_product_elements(N_G_A, N_H_B, deg_G, deg_H)
        
        neg_q = set(N_GxH_AxB) != set(N_G_A_x_N_H_B)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "H_3: A is a subgroup of G",
    "¬Q: The normalizer of A x B in G x H is not equal to N_G(A) x N_H(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3