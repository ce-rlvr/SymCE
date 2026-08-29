import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, x, y = witness
    except Exception:
        return [False] * 7
    
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

    # H_3: x and y commute
    try:
        h3 = bool(x * y == y * x)
    except Exception:
        h3 = False

    # H_4: x has finite order
    try:
        h4 = hasattr(x, 'order') and x.order() > 0
    except Exception:
        h4 = False

    # H_5: y has finite order
    try:
        h5 = hasattr(y, 'order') and y.order() > 0
    except Exception:
        h5 = False

    # H_6: The orders of x and y are coprime
    try:
        h6 = math.gcd(x.order(), y.order()) == 1
    except Exception:
        h6 = False

    # ¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G
    try:
        xy = x * y
        C_G_xy = set(g for g in G.elements if g * xy == xy * g)
        C_G_x = set(g for g in G.elements if g * x == x * g)
        C_G_y = set(g for g in G.elements if g * y == y * g)
        neg_q = C_G_xy != C_G_x.intersection(C_G_y)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: x and y commute",
    "H_4: x has finite order",
    "H_5: y has finite order",
    "H_6: The orders of x and y are coprime",
    "¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G"
]

N_HYP = 6
NEG_Q_INDEX = 6