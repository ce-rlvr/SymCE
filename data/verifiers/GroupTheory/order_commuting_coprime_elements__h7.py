import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        G, g, h = witness
    except Exception:
        return [False] * 7

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = g in G
    except Exception:
        h2 = False

    try:
        h3 = h in G
    except Exception:
        h3 = False

    try:
        h4 = (g * h == h * g)
    except Exception:
        h4 = False

    try:
        m = int(g.order())
        h5 = m > 0
    except Exception:
        h5 = False

    try:
        n = int(h.order())
        h6 = n > 0
    except Exception:
        h6 = False

    try:
        m = int(g.order())
        n = int(h.order())
        gh = g * h
        neg_q = int(gh.order()) != m * n
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: h is an element of G",
    "H_4: g and h commute (gh = hg)",
    "H_5: the order of g is a finite integer m",
    "H_6: the order of h is a finite integer n",
    "¬Q: The order of the product gh is not exactly m * n"
]

N_HYP = 6
NEG_Q_INDEX = 6