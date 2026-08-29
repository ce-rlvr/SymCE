import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, p, N, P = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(P, PermutationGroup)
        if h1:
            for gen in N.generators:
                if gen not in G:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False

    # H_3: The order of N is a power of p
    try:
        h3 = False
        if h2 and h1:
            order_N = N.order()
            temp = order_N
            while temp % p == 0:
                temp //= p
            if temp == 1:
                h3 = True
    except Exception:
        h3 = False

    # H_4: P is a Sylow p-subgroup of G
    try:
        h4 = False
        if h1 and h2:
            P_is_sub = True
            for gen in P.generators:
                if gen not in G:
                    P_is_sub = False
                    break
            if P_is_sub:
                order_G = G.order()
                order_P = P.order()
                max_pow = 1
                temp = order_G
                while temp % p == 0:
                    max_pow *= p
                    temp //= p
                if order_P == max_pow:
                    h4 = True
    except Exception:
        h4 = False

    # ¬Q: N is not a subgroup of P
    try:
        neg_q = False
        if h1:
            for gen in N.generators:
                if gen not in P:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: The order of N is a power of p",
    "H_4: P is a Sylow p-subgroup of G",
    "¬Q: N is not a subgroup of P"
]

N_HYP = 4
NEG_Q_INDEX = 4