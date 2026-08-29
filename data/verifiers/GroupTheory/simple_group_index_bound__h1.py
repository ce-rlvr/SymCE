import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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
        if len(witness) == 3:
            G, H, n = witness
        elif len(witness) == 2:
            G, H = witness
            n = G.order() // H.order()
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: H is a proper subgroup of G
    try:
        h1 = False
        if hasattr(G, 'order') and hasattr(H, 'order') and hasattr(H, 'generators'):
            if H.order() < G.order():
                if all(g in G for g in H.generators):
                    h1 = True
    except Exception:
        h1 = False

    # H_2: n is the index of H in G
    try:
        h2 = False
        if hasattr(G, 'order') and hasattr(H, 'order'):
            if n == G.order() // H.order():
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The order of G does not divide n!/2
    try:
        neg_q = False
        if hasattr(G, 'order'):
            order_G = G.order()
            fact_n_half = math.factorial(n) // 2
            if fact_n_half % order_G != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a proper subgroup of G",
    "H_2: n is the index of H in G",
    "¬Q: The order of G does not divide n!/2"
]

N_HYP = 2
NEG_Q_INDEX = 2