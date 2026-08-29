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

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False] * 6 + [False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x is an element of G
    try:
        h2 = x in G
    except Exception:
        h2 = False

    # H_3: y is an element of G
    try:
        h3 = y in G
    except Exception:
        h3 = False

    # H_4: x and y commute
    try:
        h4 = bool(x * y == y * x)
    except Exception:
        h4 = False

    # H_5: x has finite order
    try:
        h5 = x.order() > 0
    except Exception:
        h5 = False

    # H_6: y has finite order
    try:
        h6 = y.order() > 0
    except Exception:
        h6 = False

    # ¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G
    try:
        xy = x * y
        elements = list(G.generate())
        C_x = {h for h in elements if h * x == x * h}
        C_y = {h for h in elements if h * y == y * h}
        C_xy = {h for h in elements if h * xy == xy * h}
        
        neg_q = bool(C_xy != C_x.intersection(C_y))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "H_4: x and y commute",
    "H_5: x has finite order",
    "H_6: y has finite order",
    "¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G"
]

N_HYP = 6
NEG_Q_INDEX = 6