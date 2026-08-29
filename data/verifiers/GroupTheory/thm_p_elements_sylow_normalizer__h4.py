import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: The order of x is a power of p",
    "¬Q: The element x does not belong to P"
]

N_HYP = 4
NEG_Q_INDEX = 4

def is_power_of_p(n, p):
    if p <= 1:
        return False
    if n < 1:
        return False
    while n % p == 0:
        n //= p
    return n == 1

def conditions(witness):
    try:
        G, p, P, x = witness
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        h3 = False
        if h1 and h2 and isinstance(P, PermutationGroup):
            is_sub = False
            try:
                is_sub = P.is_subgroup(G)
            except Exception:
                is_sub = all(g in G for g in P.generators)
                
            if is_sub:
                order_G = G.order()
                order_P = P.order()
                if is_power_of_p(order_P, p) and (order_G // order_P) % p != 0:
                    h3 = True
    except Exception:
        h3 = False

    # H_4: The order of x is a power of p
    try:
        h4 = False
        if h1 and h2 and isinstance(x, Permutation):
            if x in G:
                if is_power_of_p(x.order(), p):
                    h4 = True
    except Exception:
        h4 = False

    # ¬Q: The element x does not belong to P
    try:
        neg_q = False
        if isinstance(P, PermutationGroup) and isinstance(x, Permutation):
            if x not in P:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]