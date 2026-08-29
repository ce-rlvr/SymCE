import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, p, P, x = witness
    except Exception:
        return [False] * 5

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H3: x is an element of the normalizer N_G(P)
    try:
        h3 = False
        if isinstance(P, PermutationGroup) and (x in G):
            # P must be a subgroup of G
            if all(g in G for g in P.generators):
                # x must normalize P
                h3 = all((x * g * ~x) in P for g in P.generators)
    except Exception:
        h3 = False

    # H4: The order of x is a power of p
    try:
        order = x.order()
        factors = factorint(order)
        h4 = all(base == p for base in factors.keys())
    except Exception:
        h4 = False

    # ¬Q: The element x does not belong to P
    try:
        neg_q = x not in P
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: x is an element of the normalizer N_G(P)",
    "H_4: The order of x is a power of p",
    "¬Q: The element x does not belong to P"
]

N_HYP = 4
NEG_Q_INDEX = 4