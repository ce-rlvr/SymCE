import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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
        G, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: e is the identity element of G
    try:
        h1 = hasattr(G, 'identity')
        if h1:
            e = G.identity
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        h2 = False
        if h1:
            h2 = x in G
    except Exception:
        h2 = False

    # H3: There exists a non-zero integer k such that x^k = e
    try:
        h3 = False
        if h1:
            if hasattr(x, 'order'):
                k = x.order()
                if k != 0 and x**k == e:
                    h3 = True
            else:
                for k in range(1, 100):
                    if x**k == e:
                        h3 = True
                        break
    except Exception:
        h3 = False

    # neg_Q: x is not equal to the identity element e
    try:
        neg_q = False
        if h1:
            neg_q = (x != e)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: e is the identity element of G",
    "H_2: x is an element of G",
    "H_3: There exists a non-zero integer k such that x^k = e",
    "¬Q: x is not equal to the identity element e"
]

N_HYP = 3
NEG_Q_INDEX = 3