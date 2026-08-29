import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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
        if len(witness) != 4:
            return [False, False, False, False]
        G, P, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if h1 and isinstance(P, PermutationGroup):
            if all(G.contains(g) for g in P.generators):
                order_G = G.order()
                order_P = P.order()
                if order_G % order_P == 0:
                    if order_P == 1:
                        h2 = True
                    else:
                        factors = factorint(order_P)
                        if len(factors) == 1:
                            p = list(factors.keys())[0]
                            if (order_G // order_P) % p != 0:
                                h2 = True
    except Exception:
        h2 = False

    # H_3: x and y are elements in the center of P
    try:
        h3 = False
        if h2:
            if P.contains(x) and P.contains(y):
                x_in_center = all(x * g == g * x for g in P.generators)
                y_in_center = all(y * g == g * y for g in P.generators)
                if x_in_center and y_in_center:
                    h3 = True
    except Exception:
        h3 = False

    # neg_Q: x and y are not conjugate in N_G(P)
    try:
        neg_q = False
        if h1 and h2 and h3:
            are_conjugate = False
            for g in G.elements:
                # Check if g normalizes P
                if all(P.contains(g * h * ~g) for h in P.generators):
                    if g * x * ~g == y:
                        are_conjugate = True
                        break
            neg_q = not are_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: x and y are elements in the center of P",
    "¬Q: x and y are not conjugate in N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3