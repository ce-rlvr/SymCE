import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, P, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group, P and H are subgroups of G
    try:
        if isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup) and isinstance(H, PermutationGroup):
            p_sub = all(G.contains(g) for g in P.generators)
            h_sub = all(G.contains(g) for g in H.generators)
            h1 = p_sub and h_sub
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        order_P = P.order()
        order_G = G.order()
        factors = factorint(order_P)
        if len(factors) == 1:
            p, k = list(factors.items())[0]
            h2 = (order_G % (p**(k+1)) != 0)
        elif order_P == 1:
            h2 = (order_G == 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: N_G(H) != H
    try:
        neg_q = False
        for g in G.generate():
            normalizes = True
            for h in H.generators:
                if not H.contains(g * h * ~g):
                    normalizes = False
                    break
            if normalizes and not H.contains(g):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group, P and H are subgroups of G",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The normalizer N_G(H) is not equal to H"
]

N_HYP = 2
NEG_Q_INDEX = 2