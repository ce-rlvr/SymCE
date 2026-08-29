import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        G, p, P, H = witness
    except Exception:
        return [False] * 5

    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            if G.order() > 0:
                h1 = True
    except Exception:
        h1 = False

    try:
        h2 = False
        if isinstance(p, (int, sympy.Integer)) and isprime(p):
            h2 = True
    except Exception:
        h2 = False

    try:
        h3 = False
        if isinstance(P, PermutationGroup) and isinstance(G, PermutationGroup):
            if hasattr(P, 'is_subgroup'):
                is_sub = bool(P.is_subgroup(G))
            else:
                is_sub = bool(all(g in G for g in P.generators))
            
            if is_sub:
                order_G = G.order()
                order_P = P.order()
                k = 0
                temp = order_G
                if temp > 0 and isinstance(p, (int, sympy.Integer)) and p > 1:
                    while temp % p == 0:
                        k += 1
                        temp //= p
                    if order_P == p**k:
                        h3 = True
    except Exception:
        h3 = False

    try:
        h4 = False
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            if hasattr(H, 'is_subgroup'):
                h4 = bool(H.is_subgroup(G))
            else:
                h4 = bool(all(g in G for g in H.generators))
    except Exception:
        h4 = False

    try:
        neg_q = False
        if h1 and h4 and h2:
            if G.order() % H.order() == 0:
                index = G.order() // H.order()
                if index % p != 1:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: H is a subgroup of G",
    "¬Q: The index of H in G is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4