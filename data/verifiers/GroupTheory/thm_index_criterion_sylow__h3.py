import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

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

def conditions(witness) -> list[bool]:
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup):
            h1 = all(g in G for g in P.generators)
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1:
            order_G = G.order()
            order_P = P.order()
            if order_G % order_P == 0:
                index = order_G // order_P
                h3 = bool(index % p != 0)
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2:
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0 and temp > 0:
                k += 1
                temp //= p
            is_sylow = (order_P == p**k)
            neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and P is a subgroup of G",
    "H_2: p is a prime number",
    "H_3: p does not divide the index of P in G",
    "¬Q: P is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3