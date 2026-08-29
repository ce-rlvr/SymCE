import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number dividing the order of G
    try:
        p_val = int(p)
        h2 = isprime(p_val) and (G.order() % p_val == 0)
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        p_val = int(p)
        if isinstance(P, PermutationGroup) and P.is_subgroup(G) and p_val > 1:
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p_val == 0:
                k += 1
                temp //= p_val
            h3 = (order_P == p_val**k)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: P is a normal subgroup of G
    try:
        if isinstance(P, PermutationGroup) and isinstance(G, PermutationGroup) and P.is_subgroup(G):
            neg_q = bool(P.is_normal(G))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P is a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3