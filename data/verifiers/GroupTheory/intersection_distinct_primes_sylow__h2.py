import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint

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

def conditions(witness) -> list[bool]:
    try:
        G, P, Q, p, q = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not isprime(p) or not P.is_subgroup(G):
            h2 = False
        else:
            order_G = G.order()
            max_pow = factorint(order_G).get(p, 0)
            h2 = (P.order() == p**max_pow)
    except Exception:
        h2 = False

    try:
        if not isprime(q) or not Q.is_subgroup(G):
            h3 = False
        else:
            order_G = G.order()
            max_pow = factorint(order_G).get(q, 0)
            h3 = (Q.order() == q**max_pow)
    except Exception:
        h3 = False

    try:
        p_elems = set(P.elements)
        q_elems = set(Q.elements)
        intersection_size = len(p_elems.intersection(q_elems))
        neg_q = intersection_size > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: Q is a Sylow q-subgroup of G",
    "¬Q: The intersection P \\cap Q is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3