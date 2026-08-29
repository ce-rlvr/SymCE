import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False, False]
        G, p, P, N = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1_ok = False

    try:
        h2_ok = isprime(p)
    except Exception:
        h2_ok = False

    try:
        if h1_ok and h2_ok and isinstance(P, PermutationGroup) and P.is_subgroup(G):
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            h3_ok = (order_P == p**k)
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    try:
        if h1_ok and h2_ok and isinstance(N, PermutationGroup) and N.is_subgroup(G):
            order_G = G.order()
            order_N = N.order()
            if order_G % order_N == 0:
                index = order_G // order_N
                if index == 1:
                    h4_ok = True
                else:
                    temp = index
                    while temp % p == 0:
                        temp //= p
                    h4_ok = (temp == 1)
            else:
                h4_ok = False
        else:
            h4_ok = False
    except Exception:
        h4_ok = False

    try:
        if h1_ok and isinstance(P, PermutationGroup) and isinstance(N, PermutationGroup) and P.is_subgroup(G) and N.is_subgroup(G):
            P_elems = list(P.generate())
            intersection_len = sum(1 for x in P_elems if x in N)
            if intersection_len == 0:
                neg_q_ok = False
            else:
                PN_len = (P.order() * N.order()) // intersection_len
                neg_q_ok = PN_len < G.order()
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: The index of N in G is a power of p",
    "not Q: G != PN"
]

N_HYP = 4
NEG_Q_INDEX = 4