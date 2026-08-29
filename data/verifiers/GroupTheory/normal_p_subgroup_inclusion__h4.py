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
        G, p, N, P = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        h3 = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup) and N.is_subgroup(G):
            h3 = True
            for g in G.generators:
                for h in N.generators:
                    if not N.contains(g * h * ~g):
                        h3 = False
                        break
                    if not N.contains(~g * h * g):
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # H_4: P is a Sylow p-subgroup of G
    try:
        h4 = False
        if isinstance(p, int) and p > 1 and isinstance(P, PermutationGroup) and isinstance(G, PermutationGroup) and P.is_subgroup(G):
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            if order_P == p**k:
                h4 = True
    except Exception:
        h4 = False

    # neg_Q: N is not a subgroup of P
    try:
        if isinstance(N, PermutationGroup) and isinstance(P, PermutationGroup):
            neg_q = not N.is_subgroup(P)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: N is a normal subgroup of G",
    "H_4: P is a Sylow p-subgroup of G",
    "¬Q: N is not a subgroup of P"
]

N_HYP = 4
NEG_Q_INDEX = 4