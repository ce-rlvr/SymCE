import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
        X = witness['X']
        Y = witness['Y']
        W = witness['W']
    except Exception:
        return [False, False, False]

    # H_1: H is a group acting faithfully on a set Y
    try:
        if isinstance(H, PermutationGroup) and isinstance(Y, (list, tuple, set)):
            # A permutation group naturally acts faithfully on its degree.
            # If len(Y) >= H.degree, it can embed in Sym(Y).
            if len(Y) >= H.degree and H.order() <= math.factorial(len(Y)):
                h1_ok = True
            else:
                h1_ok = False
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: W is the restricted wreath product of G by H
    try:
        if isinstance(W, PermutationGroup) and isinstance(G, PermutationGroup):
            # The order of the restricted wreath product of G by H acting on Y
            # is |G|^|Y| * |H|. We check this as a necessary condition.
            expected_order = (G.order() ** len(Y)) * H.order()
            if W.order() == expected_order:
                h2_ok = True
            else:
                h2_ok = False
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: W does NOT have a faithful action on X \times Y
    try:
        # W has a faithful action on X \times Y iff W embeds in Sym(X \times Y).
        # A necessary condition for embedding is |W| <= |X \times Y|!
        # If |W| > |X \times Y|!, W definitely cannot act faithfully on X \times Y.
        xy_size = len(X) * len(Y)
        if W.order() > math.factorial(xy_size):
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a group acting faithfully on a set Y",
    "H_2: W is the restricted wreath product of G by H",
    "¬Q: W does not have a faithful action on X \\times Y"
]

N_HYP = 2
NEG_Q_INDEX = 2