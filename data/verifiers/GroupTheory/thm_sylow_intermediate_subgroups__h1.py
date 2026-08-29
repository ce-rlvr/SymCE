import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def count_sylow_p_subgroups(G, P):
    P_elements = set(P.generate())
    P_gens = P.generators
    
    normalizer_size = 0
    for g in G.generate():
        normalizes = True
        for x in P_gens:
            if (g * x * ~g) not in P_elements:
                normalizes = False
                break
        if normalizes:
            normalizer_size += 1
            
    return G.order() // normalizer_size

def conditions(witness) -> list[bool]:
    try:
        G, H, P, p = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: P is a Sylow p-subgroup of G
    try:
        P_is_sub_G = all(g in G for g in P.generators)
        G_order = G.order()
        k = 0
        temp = G_order
        while temp > 0 and temp % p == 0:
            k += 1
            temp //= p
        expected_P_order = p**k
        h2 = bool(P_is_sub_G and P.order() == expected_P_order)
    except Exception:
        h2 = False
        
    # H_3: H is a subgroup of G that contains P
    try:
        H_is_sub_G = all(g in G for g in H.generators)
        H_contains_P = all(g in H for g in P.generators)
        h3 = bool(H_is_sub_G and H_contains_P)
    except Exception:
        h3 = False
        
    # ¬Q: P is not a Sylow p-subgroup of H, OR n_p(H) does not divide n_p(G)
    try:
        H_order = H.order()
        k_H = 0
        temp_H = H_order
        while temp_H > 0 and temp_H % p == 0:
            k_H += 1
            temp_H //= p
        expected_P_order_H = p**k_H
        P_is_sub_H = all(g in H for g in P.generators)
        P_is_sylow_H = P_is_sub_H and (P.order() == expected_P_order_H)
        
        if not P_is_sylow_H:
            neg_q = True
        else:
            n_p_H = count_sylow_p_subgroups(H, P)
            n_p_G = count_sylow_p_subgroups(G, P)
            neg_q = bool(n_p_G % n_p_H != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: H is a subgroup of G that contains P",
    "¬Q: P is not a Sylow p-subgroup of H, or the number of Sylow p-subgroups of H does not divide the number of Sylow p-subgroups of G"
]

N_HYP = 3
NEG_Q_INDEX = 3