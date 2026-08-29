import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import isprime

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

def get_normalizer(G, H):
    H_elements = set(H.generate())
    norm_elements = []
    for g in G.generate():
        is_normalizer = True
        for h in H.generators:
            if (g * h * ~g) not in H_elements:
                is_normalizer = False
                break
        if is_normalizer:
            norm_elements.append(g)
    return PermutationGroup(norm_elements)

def conditions(witness):
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False]
    
    # H_1: Let p be a prime number dividing the order of G.
    try:
        h1 = isprime(p) and (G.order() % p == 0)
    except Exception:
        h1 = False
        
    # H_2: Let P be a Sylow p-subgroup of G.
    try:
        is_subgroup = all(g in G for g in P.generators)
        if is_subgroup:
            order = P.order()
            g_order = G.order()
            expected_order = 1
            while g_order % p == 0:
                expected_order *= p
                g_order //= p
            h2 = (order == expected_order)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: N_G(N_G(P)) != N_G(P)
    try:
        N1 = get_normalizer(G, P)
        N2 = get_normalizer(G, N1)
        neg_q = (N1.order() != N2.order())
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing the order of G",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: N_G(N_G(P)) != N_G(P)"
]

N_HYP = 2
NEG_Q_INDEX = 2