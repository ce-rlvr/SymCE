import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
        G, p, P, x = witness
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

    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        elif not all(G.contains(g) for g in P.generators):
            h3 = False
        else:
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            h3 = (order_P == p**k)
    except Exception:
        h3 = False

    # H_4: x is an element of the normalizer N_G(P)
    try:
        if not isinstance(x, Permutation):
            h4 = False
        elif not G.contains(x):
            h4 = False
        else:
            h4 = True
            for g in P.generators:
                if not P.contains(~x * g * x):
                    h4 = False
                    break
    except Exception:
        h4 = False

    # neg_Q: x does not belong to P
    try:
        if not isinstance(x, Permutation):
            neg_q = False
        else:
            neg_q = not P.contains(x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: x is an element of the normalizer N_G(P)",
    "¬Q: x does not belong to P"
]

N_HYP = 4
NEG_Q_INDEX = 4