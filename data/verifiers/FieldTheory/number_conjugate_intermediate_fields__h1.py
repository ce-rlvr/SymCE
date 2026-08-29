import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

def group_order(G):
    try:
        return G.order()
    except TypeError:
        return G.order

def get_elements(G):
    try:
        return list(G.elements)
    except Exception:
        return list(G.generate())

def groups_equal(G1, G2):
    if group_order(G1) != group_order(G2):
        return False
    for g in G1.generators:
        if g not in G2:
            return False
    return True

def get_normalizer(G, H):
    gens = H.generators
    norm_elements = []
    for g in get_elements(G):
        if all((g * h * ~g) in H for h in gens):
            norm_elements.append(g)
    if not norm_elements:
        norm_elements = [Permutation()]
    return PermutationGroup(norm_elements)

def conditions(witness):
    """
    Witness should be a tuple (Gamma, U, W) of sympy PermutationGroups
    representing the Galois correspondence:
    Gamma = Gal(M/K) for some normal closure M
    U = Gal(M/L)
    W = Gal(M/E)
    """
    try:
        Gamma, U, W = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is the Galois group of L/K
    try:
        h1 = U.is_subgroup(Gamma)
    except Exception:
        h1 = False
        
    # H_2: E is an intermediate field between K and L
    try:
        h2 = W.is_subgroup(Gamma) and U.is_subgroup(W)
    except Exception:
        h2 = False
        
    # H_3: H is the subgroup of G fixing E
    try:
        h3 = isinstance(Gamma, PermutationGroup) and isinstance(U, PermutationGroup) and isinstance(W, PermutationGroup)
    except Exception:
        h3 = False
        
    # neg_Q: The number of distinct intermediate fields conjugate to E over K is NOT equal to the index of N_G(H) in G
    try:
        # G corresponds to N_Gamma(U) / U
        N_Gamma_U = get_normalizer(Gamma, U)
        
        # H corresponds to N_W(U) / U
        N_W_U = get_normalizer(W, U)
        
        # N_G(H) corresponds to N_{N_Gamma(U)}(N_W(U)) / U
        N_G_H = get_normalizer(N_Gamma_U, N_W_U)
        
        # Index of N_G(H) in G
        index = group_order(N_Gamma_U) // group_order(N_G_H)
        
        # Number of distinct intermediate fields conjugate to E over K
        # These correspond to subgroups gamma W gamma^-1 that contain U, for gamma in Gamma
        conjugates_of_W = []
        for gamma in get_elements(Gamma):
            # Check if U <= gamma W gamma^-1 (equivalent to gamma^-1 U gamma <= W)
            if all((~gamma * u * gamma) in W for u in U.generators):
                conj_gens = [gamma * w * ~gamma for w in W.generators]
                if not conj_gens:
                    conj_gens = [gamma * ~gamma]
                conj_W = PermutationGroup(conj_gens)
                
                is_new = True
                for C in conjugates_of_W:
                    if groups_equal(conj_W, C):
                        is_new = False
                        break
                if is_new:
                    conjugates_of_W.append(conj_W)
        c = len(conjugates_of_W)
        
        neg_q = (c != index)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is the Galois group of L/K",
    "H_2: E is an intermediate field between K and L",
    "H_3: H is the subgroup of G fixing E",
    "¬Q: The number of distinct intermediate fields conjugate to E over K is NOT equal to the index of N_G(H) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3