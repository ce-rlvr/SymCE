import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group and N is a subgroup of G
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
            h1 = False
        else:
            h1 = True
            for gen in N.generators:
                if gen not in G:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: The order of N and the index of N in G are coprime
    try:
        if not h1:
            h2 = False
        else:
            order_G = G.order()
            order_N = N.order()
            if order_G % order_N != 0:
                h2 = False
            else:
                index = order_G // order_N
                h2 = math.gcd(order_N, index) == 1
    except Exception:
        h2 = False

    # neg_Q: There is no subgroup H such that G is the internal semidirect product of N and H
    try:
        if not h1:
            neg_q = False
        else:
            order_G = G.order()
            order_N = N.order()
            if order_G % order_N != 0:
                neg_q = False
            else:
                # For G to be the internal semidirect product of N and H,
                # N must be a normal subgroup of G.
                # If N is not normal, G cannot be the internal semidirect product of N and H.
                if not N.is_normal(G):
                    neg_q = True
                else:
                    # If N is normal, Schur-Zassenhaus theorem guarantees that H exists,
                    # so the conclusion holds (neg_q is False).
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and N is a subgroup of G",
    "H_2: The order of N and the index of N in G are coprime",
    "¬Q: There is no subgroup H such that G is the internal semidirect product of N and H"
]

N_HYP = 2
NEG_Q_INDEX = 2