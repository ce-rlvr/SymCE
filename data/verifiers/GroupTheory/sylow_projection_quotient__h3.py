import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_power(n, p):
    n = int(n)
    p = int(p)
    if n <= 0:
        return False
    if n == 1:
        return True
    if p <= 1:
        return n == 1
    while n % p == 0:
        n //= p
    return n == 1

def get_elements(H, degree):
    els = set()
    for p in H.generate():
        arr = p.array_form
        if len(arr) < degree:
            arr = arr + list(range(len(arr), degree))
        els.add(tuple(arr))
    return els

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, N, P, p = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = False
        if h1 and isinstance(N, PermutationGroup):
            if N.is_subgroup(G):
                h2 = N.is_normal(G)
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        h3 = False
        if h1 and isinstance(P, PermutationGroup):
            try:
                p_val = int(p)
                valid_p = (p_val >= 2 and p_val == p)
            except Exception:
                valid_p = False
            
            if valid_p and P.is_subgroup(G):
                order_P = P.order()
                order_G = G.order()
                if is_power(order_P, p_val):
                    index = order_G // order_P
                    if math.gcd(int(index), p_val) == 1:
                        h3 = True
    except Exception:
        h3 = False

    # neg_Q: PN/N is NOT a Sylow p-subgroup of G/N
    try:
        neg_q = False
        if h1 and h2 and h3:
            p_val = int(p)
            degree = max(G.degree, P.degree, N.degree)
            P_els = get_elements(P, degree)
            N_els = get_elements(N, degree)
            intersection_len = len(P_els.intersection(N_els))
            
            order_PN = (P.order() * N.order()) // intersection_len
            order_PN_mod_N = order_PN // N.order()
            index_PN_mod_N = G.order() // order_PN
            
            is_sylow = is_power(order_PN_mod_N, p_val) and (math.gcd(int(index_PN_mod_N), p_val) == 1)
            neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: PN/N is not a Sylow p-subgroup of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3