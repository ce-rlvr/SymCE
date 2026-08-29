import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_unique_sylow(G, p):
    if not isprime(p):
        return False
    n = G.order()
    if n % p != 0:
        return True
    P = G.sylow_subgroup(p)
    for g in G.generators:
        for h in P.generators:
            if (g * h * g**-1) not in P:
                return False
    return True

def is_cyclic_of_order(G, m):
    if G.order() != m:
        return False
    if m == 1:
        return True
    for g in G.elements:
        if g.order() == m:
            return True
    return False

def conditions(witness):
    try:
        G, p, q = witness
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p and q are prime numbers
    try:
        h2 = bool(isprime(p) and isprime(q))
    except Exception:
        h2 = False

    # H_3: p is strictly less than q
    try:
        h3 = bool(p < q)
    except Exception:
        h3 = False

    # H_4: p does not divide q - 1
    try:
        h4 = bool((q - 1) % p != 0)
    except Exception:
        h4 = False

    # ¬Q: G does not have a unique normal Sylow p-subgroup, or does not have a unique normal Sylow q-subgroup, or is not isomorphic to the cyclic group of order pq
    try:
        c1 = is_unique_sylow(G, p)
        c2 = is_unique_sylow(G, q)
        c3 = is_cyclic_of_order(G, p * q)
        q_val = c1 and c2 and c3
        neg_q = not q_val
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are prime numbers",
    "H_3: p is strictly less than q",
    "H_4: p does not divide q - 1",
    "¬Q: G does not have a unique normal Sylow p-subgroup, or does not have a unique normal Sylow q-subgroup, or is not isomorphic to the cyclic group of order pq"
]

N_HYP = 4
NEG_Q_INDEX = 4