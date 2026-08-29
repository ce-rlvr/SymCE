import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def is_power_of(n, p):
    if n == 1: 
        return True
    if p <= 1: 
        return False
    while n % p == 0 and n > 1:
        n //= p
    return n == 1

def conditions(witness) -> list[bool]:
    try:
        G, P, N, p = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and G.order() < float('inf')
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if sympy.isprime(p) and hasattr(P, 'is_subgroup') and P.is_subgroup(G):
            order_P = P.order()
            if is_power_of(order_P, p):
                order_G = G.order()
                highest_power = 1
                temp = order_G
                while temp % p == 0 and temp > 0:
                    highest_power *= p
                    temp //= p
                h2 = (order_P == highest_power)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        h3 = hasattr(N, 'is_subgroup') and N.is_subgroup(G) and hasattr(N, 'is_normal') and N.is_normal(G)
    except Exception:
        h3 = False

    # H_4: The index of N in G is a power of p
    try:
        index = G.order() // N.order()
        h4 = is_power_of(index, p)
    except Exception:
        h4 = False

    # neg_Q: G != PN
    try:
        P_elems = list(P.generate())
        N_elems = list(N.generate())
        PN_set = set()
        for x in P_elems:
            for y in N_elems:
                PN_set.add(x * y)
        neg_q = len(PN_set) != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: N is a normal subgroup of G",
    "H_4: The index of N in G is a power of p",
    "¬Q: G != PN"
]

N_HYP = 4
NEG_Q_INDEX = 4